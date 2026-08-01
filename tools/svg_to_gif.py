#!/usr/bin/env python3
"""Convert animated SVG files to GIFs.

The converter renders SVG animation frames with a system Chrome (via
``chrome_render``), captures each frame, crops to the visible
animation bounds, resizes to a square target canvas, and writes an animated GIF.

The crop window is clamped to a fixed range of viewBox *units* (not raw pixels),
so Clawd's body always occupies a controlled fraction of the output frame. A
tight animation gets whitespace padded around it instead of being blown up to
fill the canvas; the documented 20-33 unit frame range maps directly to the
55%-34% torso-size range Clawd is allowed to occupy.
"""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image

import chrome_render


DEFAULT_VIEWPORT = chrome_render.DEFAULT_VIEWPORT
DEFAULT_DURATION_MS = 3000


MIN_FPS = 20

# Clawd's documented on-frame size range, expressed as the side of the square
# crop window in viewBox *units*. The torso is 11 units wide, so a 20-unit window
# puts the torso at ~55% (largest allowed, cf. clawd-surrender-helpless) and a
# 33-unit window at ~34% (smallest, cf. clawd-kick-football). Clamping the crop
# window to this range is what actually controls body size in the exported GIF.
DEFAULT_MIN_UNITS = 20.0
DEFAULT_MAX_UNITS = 33.0


def default_workers() -> int:
    """Pick a safe concurrency: a few parallel Chromes, leaving a core free."""
    return max(1, min(4, (os.cpu_count() or 2) - 1))


@dataclass(frozen=True)
class ExportOptions:
    size: int
    fps: int
    padding: int
    alpha_threshold: int
    background: str
    hide_ground_shadow: bool
    workers: int
    timeout: float
    min_units: float
    max_units: float
    max_duration_ms: int | None = None


def parse_viewbox(svg_text: str) -> tuple[float, float, float, float] | None:
    """Return the SVG viewBox as (min_x, min_y, width, height), if present."""
    match = re.search(r'viewBox\s*=\s*"([^"]+)"', svg_text)
    if not match:
        return None
    parts = re.split(r"[\s,]+", match.group(1).strip())
    if len(parts) != 4:
        return None
    try:
        min_x, min_y, width, height = (float(value) for value in parts)
    except ValueError:
        return None
    if width <= 0 or height <= 0:
        return None
    return (min_x, min_y, width, height)



def parse_duration_ms(svg_text: str, fallback_ms: int = DEFAULT_DURATION_MS) -> int:
    """Return the longest CSS animation duration in milliseconds."""
    durations: list[float] = []

    for match in re.finditer(r"animation(?:-duration)?\s*:\s*([^;}]+)(?:;|})", svg_text):
        value = match.group(1)
        for duration, unit in re.findall(r"([\d.]+)\s*(ms|s)\b", value):
            amount = float(duration)
            durations.append(amount if unit == "ms" else amount * 1000)

    return int(max(durations)) if durations else fallback_ms


def iter_svg_inputs(input_path: Path) -> list[Path]:
    if input_path.is_file():
        if input_path.suffix.lower() != ".svg":
            raise ValueError(f"input file is not an SVG: {input_path}")
        return [input_path]
    if input_path.is_dir():
        return sorted(input_path.glob("*.svg"))
    raise FileNotFoundError(input_path)


def resolve_output_path(svg_path: Path, input_path: Path, output_path: Path | None) -> Path:
    if output_path is None:
        return svg_path.with_suffix(".gif")
    if len(iter_svg_inputs(input_path)) == 1 and output_path.suffix.lower() == ".gif":
        return output_path
    return output_path / f"{svg_path.stem}.gif"


def render_frames(svg_path: Path, options: ExportOptions, chrome: str | None) -> list[Image.Image]:
    svg_text = svg_path.read_text(encoding="utf-8")
    source_duration_ms = parse_duration_ms(svg_text)
    output_duration_ms = source_duration_ms
    if options.max_duration_ms:
        output_duration_ms = min(output_duration_ms, options.max_duration_ms)
    frame_count = max(1, round(output_duration_ms * options.fps / 1000))
    # Sample the complete source cycle even when compressing it to a shorter GIF.
    times_ms = [i * source_duration_ms / frame_count for i in range(frame_count)]

    mode = "serial" if options.workers <= 1 else f"{options.workers} workers"

    def progress(done: int, total: int) -> None:
        print(f"\r  {svg_path.name}: rendering {done}/{total} frames ({mode})", end="", flush=True)

    background = "transparent" if options.background == "transparent" else "white"
    frames = chrome_render.render_frames(
        svg_text,
        times_ms,
        viewport=DEFAULT_VIEWPORT,
        background=background,
        hide_shadow=options.hide_ground_shadow,
        chrome=chrome,
        workers=options.workers,
        timeout=options.timeout,
        progress=progress,
    )
    print()  # finish the progress line
    return frames


def content_bounds(frames: list[Image.Image], alpha_threshold: int) -> tuple[int, int, int, int] | None:
    """Tight pixel bounding box of all non-transparent content across frames."""
    x0, y0 = frames[0].size
    x1 = y1 = 0
    found = False

    for frame in frames:
        alpha = np.array(frame.getchannel("A"))
        mask = alpha > alpha_threshold
        if not mask.any():
            continue
        found = True
        ys, xs = np.where(mask)
        x0 = min(x0, int(xs.min()))
        y0 = min(y0, int(ys.min()))
        x1 = max(x1, int(xs.max()) + 1)
        y1 = max(y1, int(ys.max()) + 1)

    if not found or x1 <= x0 or y1 <= y0:
        return None
    return (x0, y0, x1, y1)


def crop_bounds(
    frames: list[Image.Image],
    padding: int,
    alpha_threshold: int,
    px_per_unit: float | None,
    min_units: float,
    max_units: float,
) -> tuple[int, int, int, int]:
    """Square crop window around the animation content.

    The window side is driven by viewBox *units* when ``px_per_unit`` is known:
    it is at least ``min_units`` and at most ``max_units`` wide, so a compact
    animation is padded with whitespace rather than zoomed up to fill the canvas.
    This is what bounds Clawd's body size in the exported GIF. Without a viewBox
    (``px_per_unit`` is None) it falls back to a tight content-fitted crop.
    """
    frame_w, frame_h = frames[0].size
    content = content_bounds(frames, alpha_threshold)
    if content is None:
        return (0, 0, frame_w, frame_h)
    x0, y0, x1, y1 = content

    x0 = max(0, x0 - padding)
    y0 = max(0, y0 - padding)
    x1 = min(frame_w, x1 + padding)
    y1 = min(frame_h, y1 + padding)

    width, height = x1 - x0, y1 - y0
    side = max(width, height)

    if px_per_unit:
        # Clamp the window to the documented unit range. A window smaller than
        # min_units would make Clawd too large (over-cropped); larger than
        # max_units would make Clawd too small (too much whitespace).
        side = max(side, round(min_units * px_per_unit))
        side = min(side, round(max_units * px_per_unit))

    side = min(side, frame_w, frame_h)

    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    sx0 = max(0, min(frame_w - side, cx - side // 2))
    sy0 = max(0, min(frame_h - side, cy - side // 2))
    return (sx0, sy0, sx0 + side, sy0 + side)


def prepare_gif_frames(
    frames: list[Image.Image],
    options: ExportOptions,
    px_per_unit: float | None,
) -> list[Image.Image]:
    bounds = crop_bounds(
        frames,
        options.padding,
        options.alpha_threshold,
        px_per_unit,
        options.min_units,
        options.max_units,
    )
    prepared: list[Image.Image] = []

    for frame in frames:
        cropped = frame.crop(bounds).resize((options.size, options.size), Image.Resampling.LANCZOS)

        if options.background != "transparent":
            canvas = Image.new("RGBA", cropped.size, options.background)
            canvas.alpha_composite(cropped)
            prepared.append(canvas.convert("RGB").convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
            continue

        rgba = np.array(cropped, dtype=np.float32)
        rgb, alpha = rgba[..., :3], rgba[..., 3:4]
        ratio = alpha / 255.0
        blended_rgb = rgb * ratio + 255.0 * (1.0 - ratio)
        binary_alpha = np.where(alpha > options.alpha_threshold, 255.0, 0.0)
        blended = np.concatenate([blended_rgb, binary_alpha], axis=-1).clip(0, 255).astype(np.uint8)
        image = Image.fromarray(blended).convert("RGBA")
        palette_image = image.convert("RGB").convert("P", palette=Image.Palette.ADAPTIVE, colors=255)
        mask = Image.eval(image.getchannel("A"), lambda value: 255 if value <= options.alpha_threshold else 0)
        palette_image.paste(255, mask)
        palette_image.info["transparency"] = 255
        prepared.append(palette_image)

    return prepared


def export_svg(svg_path: Path, output_path: Path, options: ExportOptions, chrome: str | None) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    svg_text = svg_path.read_text(encoding="utf-8")
    viewbox = parse_viewbox(svg_text)
    px_per_unit = DEFAULT_VIEWPORT / viewbox[2] if viewbox else None
    frames = render_frames(svg_path, options, chrome)
    gif_frames = prepare_gif_frames(frames, options, px_per_unit)
    frame_duration_ms = int(1000 / options.fps)

    save_kwargs = {
        "save_all": True,
        "append_images": gif_frames[1:],
        "duration": frame_duration_ms,
        "loop": 0,
    }
    if options.background == "transparent":
        save_kwargs["disposal"] = 2

    gif_frames[0].save(output_path, **save_kwargs)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"{svg_path} -> {output_path} ({len(gif_frames)} frames, {size_kb:.1f} KB)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert animated SVG files to GIFs.")
    parser.add_argument("--input", "-i", required=True, type=Path, help="SVG file or directory of SVG files.")
    parser.add_argument("--output", "-o", type=Path, help="GIF file path for single input, or output directory.")
    parser.add_argument("--size", type=int, default=240, help="Output GIF width and height in pixels.")
    parser.add_argument("--fps", type=int, default=MIN_FPS, help=f"Frames per second (clamped to a minimum of {MIN_FPS}).")
    parser.add_argument("--padding", type=int, default=6, help="Padding around detected animation bounds.")
    parser.add_argument(
        "--min-units",
        type=float,
        default=DEFAULT_MIN_UNITS,
        help="Smallest crop window in viewBox units (caps Clawd's max on-frame size). 0 disables the lower clamp.",
    )
    parser.add_argument(
        "--max-units",
        type=float,
        default=DEFAULT_MAX_UNITS,
        help="Largest crop window in viewBox units (caps Clawd's min on-frame size / max whitespace).",
    )
    parser.add_argument("--alpha-threshold", type=int, default=128, help="Alpha cutoff for transparent GIF output.")
    parser.add_argument(
        "--background",
        choices=["transparent", "white"],
        default="transparent",
        help="Transparent GIFs are compact; white background is safer for WeChat-style clients.",
    )
    parser.add_argument(
        "--keep-ground-shadow",
        action="store_true",
        help="Keep the ground shadow rect instead of hiding it before capture.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=default_workers(),
        help="Concurrent Chrome renders (auto by CPU). Use --workers 1 for the serial safe baseline.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=chrome_render.DEFAULT_TIMEOUT,
        help="Hard timeout (seconds) per frame render; a hung Chrome is killed past this.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    svg_paths = iter_svg_inputs(args.input)
    if not svg_paths:
        raise SystemExit(f"No SVG files found in {args.input}")

    fps = max(MIN_FPS, args.fps)
    if fps != args.fps:
        print(f"fps raised to the minimum of {MIN_FPS} (was {args.fps}).")

    options = ExportOptions(
        size=args.size,
        fps=fps,
        padding=args.padding,
        alpha_threshold=args.alpha_threshold,
        background="#ffffff" if args.background == "white" else "transparent",
        hide_ground_shadow=not args.keep_ground_shadow,
        workers=max(1, args.workers),
        timeout=args.timeout,
        min_units=max(0.0, args.min_units),
        max_units=args.max_units,
    )

    chrome = chrome_render.find_chrome()
    if not chrome:
        raise SystemExit("No Chrome found. Set CHROME=/path/to/chrome and retry.")

    for svg_path in svg_paths:
        output_path = resolve_output_path(svg_path, args.input, args.output)
        export_svg(svg_path, output_path, options, chrome)


if __name__ == "__main__":
    main()
