#!/usr/bin/env python3
"""Render animated SVG frames with a system Chrome.

The whole toolchain renders through a system Chrome/Chromium binary, so setup is
just `pip install pillow numpy` plus a Chrome you already have. Each frame is
rendered in its own short-lived Chrome process with an isolated `--user-data-dir`
profile and a hard timeout: if a headless Chrome ever hangs, its whole process
group is killed so the export can never stall forever. Frames render serially by
default (the safe baseline); pass workers>1 to opt into
parallel rendering. Each frame seeks the animation to an exact time via the Web
Animations API so per-element stagger is preserved.
"""
from __future__ import annotations

import glob
import html as html_lib
import io
import os
import signal
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image

DEFAULT_VIEWPORT = 500
DEFAULT_TIMEOUT = 30.0  # seconds per frame; a hung Chrome is killed past this
_VIRTUAL_TIME_MS = 1500


def find_chrome() -> str | None:
    """Locate a Chrome/Chromium binary (CHROME env var, common paths, caches)."""
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


def _frame_html(svg_text: str, viewport: int, time_ms: float, background: str, hide_shadow: bool) -> str:
    bg = "#ffffff" if background == "white" else "transparent"
    shadow_css = 'rect[y="15"][fill="#000000"]{display:none!important}' if hide_shadow else ""
    seek = (
        "<script>addEventListener('DOMContentLoaded',function(){"
        "document.getAnimations().forEach(function(a){a.pause();a.currentTime=__T__;});"
        "});</script>"
    ).replace("__T__", repr(float(time_ms)))
    css = (
        "html,body{margin:0;padding:0;overflow:hidden;background:%s}"
        "svg{width:%dpx;height:%dpx}%s" % (bg, viewport, viewport, shadow_css)
    )
    return (
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        + css
        + "</style></head><body>"
        + svg_text
        + seek
        + "</body></html>"
    )


def _kill_group(proc: "subprocess.Popen") -> None:
    """Kill the whole Chrome process group (browser + helper processes)."""
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except (ProcessLookupError, PermissionError, OSError):
        proc.kill()
    try:
        proc.wait(timeout=5)
    except Exception:
        pass


def _render_one(args) -> "Image.Image":
    chrome, svg_text, viewport, time_ms, background, hide_shadow, timeout = args
    html = _frame_html(svg_text, viewport, time_ms, background, hide_shadow)
    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / "frame.html"
        png_path = Path(tmp) / "frame.png"
        html_path.write_text(html, encoding="utf-8")
        # --headless=new already gives each process its own ephemeral profile, so
        # concurrent renders don't share a profile lock. (An explicit
        # --user-data-dir would keep Chrome alive after the screenshot — avoid it.)
        cmd = [
            chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--no-first-run", "--no-default-browser-check",
            "--force-device-scale-factor=1",
            "--run-all-compositor-stages-before-draw",
            f"--virtual-time-budget={_VIRTUAL_TIME_MS}",
            f"--window-size={viewport},{viewport}",
            f"--screenshot={png_path}", html_path.resolve().as_uri(),
        ]
        if background != "white":
            cmd.insert(1, "--default-background-color=00000000")
        # Own session/process group + hard timeout: a hung Chrome (and its
        # helpers) gets killed instead of stalling the whole export forever.
        proc = subprocess.Popen(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            _kill_group(proc)
            raise RuntimeError(f"Chrome render timed out after {timeout:.0f}s (killed) at {time_ms}ms")
        if not png_path.exists():
            raise RuntimeError(f"Chrome produced no screenshot (time={time_ms}ms)")
        return Image.open(io.BytesIO(png_path.read_bytes())).convert("RGBA")


def render_frames(
    svg_text: str,
    times_ms,
    *,
    viewport: int = DEFAULT_VIEWPORT,
    background: str = "transparent",
    hide_shadow: bool = False,
    chrome: str | None = None,
    workers: int = 1,
    timeout: float = DEFAULT_TIMEOUT,
    progress=None,
) -> list["Image.Image"]:
    """Render the SVG at each animation time (ms) to a list of RGBA frames.

    Serial by default (``workers=1``) — the safe baseline. Raise ``workers`` to
    render frames in parallel; each frame still gets an isolated profile and a
    hard ``timeout``. ``progress(done, total)`` is called after each frame.
    """
    chrome = chrome or find_chrome()
    if not chrome:
        raise RuntimeError("No Chrome found. Set CHROME=/path/to/chrome and retry.")
    jobs = [
        (chrome, svg_text, viewport, t, background, hide_shadow, timeout)
        for t in times_ms
    ]
    total = len(jobs)
    frames: list = [None] * total

    if workers <= 1:
        for index, job in enumerate(jobs):
            frames[index] = _render_one(job)
            if progress:
                progress(index + 1, total)
        return frames

    done = 0
    with ThreadPoolExecutor(max_workers=min(workers, total)) as pool:
        future_to_index = {pool.submit(_render_one, job): i for i, job in enumerate(jobs)}
        for future in as_completed(future_to_index):
            frames[future_to_index[future]] = future.result()
            done += 1
            if progress:
                progress(done, total)
    return frames
