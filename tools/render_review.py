#!/usr/bin/env python3
"""render_review.py — render animations to PNGs + a contact sheet for visual review.

Static source checks cannot see a hat that floats, a leg that detaches, or a prop
that drifts off the hand at render time. Pixel-art SVG "lies" in the source: it
can look attached in the code and break in the browser. The only reliable check
is to LOOK at a real render. This renders each animation SVG with a headless
Chrome and assembles a contact sheet, so you (or the agent) can READ the images
and verify each animation actually looks right.

It drives a system Chrome directly. Honors the CHROME env var.

Usage:
    python3 tools/render_review.py [--input DIR_OR_SVG ...] [--out DIR]
                                   [--pause SECONDS] [--cols N] [--max N]

Then READ the contact sheet (and the per-animation PNGs) under the output dir.
Each SVG is rendered in isolation so their global CSS class names never collide.
"""
from __future__ import annotations

import argparse
import glob
import math
import os
import signal
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUTS = [
    ROOT / "assets" / "upstream" / "svg",
    ROOT / "assets" / "original" / "svg",
    ROOT / "assets" / "generated" / "svg",
]
DEFAULT_OUT = Path("/tmp/clawd-review")
TILE = 200  # rendered size (CSS px) per animation


def find_chrome() -> str | None:
    """Locate a Chrome/Chromium binary robustly (env var, common paths, caches)."""
    env = os.environ.get("CHROME")
    if env and Path(env).exists():
        return env
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ]
    home = str(Path.home())
    patterns = [
        home + "/Library/Caches/ms-playwright/chromium*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium",
        home + "/.cache/ms-playwright/chromium*/chrome-linux/chrome",
        home + "/.cache/puppeteer/chrome/*/**/Google Chrome for Testing",
        home + "/.cache/puppeteer/chrome/*/**/chrome",
    ]
    for pattern in patterns:
        candidates += sorted(glob.glob(pattern, recursive=True))
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return None


def iter_svgs(inputs: list) -> list[Path]:
    found: list[Path] = []
    for item in inputs:
        path = Path(item)
        path = path if path.is_absolute() else ROOT / path
        if path.is_file() and path.suffix == ".svg":
            found.append(path)
        elif path.is_dir():
            found.extend(sorted(path.glob("*.svg")))
    return sorted(dict.fromkeys(found))


def wrap_html(svg_text: str, pause: float | None) -> str:
    freeze = ""
    if pause is not None:
        freeze = (
            "*{animation-delay:-%ss!important;animation-play-state:paused!important}"
            % pause
        )
    return (
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        "html,body{margin:0;width:%dpx;height:%dpx;background:#fff;overflow:hidden}"
        "svg{width:%dpx;height:%dpx}%s</style></head><body>%s</body></html>"
        % (TILE, TILE, TILE, TILE, freeze, svg_text)
    )


def render_one(chrome: str, svg_path: Path, out_png: Path, pause: float | None) -> bool:
    html_path = out_png.with_suffix(".html")
    html_path.write_text(wrap_html(svg_path.read_text(encoding="utf-8"), pause), encoding="utf-8")
    cmd = [
        chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--no-first-run", "--no-default-browser-check",
        "--force-device-scale-factor=2", f"--window-size={TILE},{TILE}",
        f"--screenshot={out_png}", html_path.resolve().as_uri(),
    ]
    # Own process group + hard timeout so a hung Chrome can't stall the review.
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            start_new_session=True)
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except OSError:
            proc.kill()
    html_path.unlink(missing_ok=True)
    return out_png.exists()


def build_contact_sheet(items: list[tuple[str, Path]], out: Path, cols: int) -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("(install Pillow to assemble the contact sheet)")
        return
    if not items:
        return
    pad, label_h = 6, 16
    tile_w, tile_h = Image.open(items[0][1]).size
    cell_w, cell_h = tile_w + pad * 2, tile_h + label_h + pad * 2
    rows = math.ceil(len(items) / cols)
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for index, (name, png) in enumerate(items):
        row, col = divmod(index, cols)
        x, y = col * cell_w + pad, row * cell_h + pad
        sheet.paste(Image.open(png), (x, y))
        draw.text((x, y + tile_h + 2), name, fill="black", font=font)
    sheet_path = out / "contact.png"
    sheet.save(sheet_path)
    print(f"contact sheet -> {sheet_path}  ({len(items)} animations) — now READ it")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render animations for visual review.")
    parser.add_argument("--input", nargs="+", default=None, help="SVG files or dirs.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--pause", type=float, default=None,
                        help="freeze animations at this many seconds (default: live first frame)")
    parser.add_argument("--cols", type=int, default=6)
    parser.add_argument("--max", type=int, default=None, help="limit number of SVGs")
    args = parser.parse_args()

    chrome = find_chrome()
    if not chrome:
        print("No Chrome found. Set CHROME=/path/to/chrome and retry.")
        return 2
    print(f"using chrome: {chrome}")

    svgs = iter_svgs(args.input if args.input else DEFAULT_INPUTS)
    if args.max:
        svgs = svgs[: args.max]
    if not svgs:
        print("No SVG files found.")
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    rendered: list[tuple[str, Path]] = []
    failed: list[str] = []
    for svg in svgs:
        png = args.out / f"{svg.stem}.png"
        if render_one(chrome, svg, png, args.pause):
            rendered.append((svg.stem, png))
        else:
            failed.append(svg.stem)
    print(f"rendered {len(rendered)}/{len(svgs)} -> {args.out}/")
    if failed:
        print(f"FAILED to render: {', '.join(failed)}")
    build_contact_sheet(rendered, args.out, args.cols)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
