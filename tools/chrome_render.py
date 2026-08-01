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
    shadow_hider = ""
    if hide_shadow:
        # Models do not consistently use the canonical y=15 ground-shadow rect.
        # Detect only flat, dark shapes near the bottom of the SVG so eyes,
        # limbs, and opaque props such as keyboards remain untouched.
        shadow_hider = """<script>addEventListener('DOMContentLoaded',function(){
const svg=document.querySelector('svg');if(!svg)return;
const canvas=svg.getBoundingClientRect();if(!canvas.width||!canvas.height)return;
svg.querySelectorAll('rect,ellipse,line,path,polygon,polyline').forEach(function(el){
  const label=((el.id||'')+' '+(el.getAttribute('class')||'')).toLowerCase();
  const box=el.getBoundingClientRect();
  const style=getComputedStyle(el);
  const fill=(style.fill||'').replace(/\\s+/g,'').toLowerCase();
  const stroke=(style.stroke||'').replace(/\\s+/g,'').toLowerCase();
  const black=['#000','#000000','black','rgb(0,0,0)','rgba(0,0,0,1)'];
  const dark=black.includes(fill)||black.includes(stroke);
  const ownOpacity=parseFloat(style.opacity||'1');
  const paintOpacity=Math.min(
    Number.isFinite(parseFloat(style.fillOpacity))?parseFloat(style.fillOpacity):1,
    Number.isFinite(parseFloat(style.strokeOpacity))?parseFloat(style.strokeOpacity):1
  );
  const opacity=(Number.isFinite(ownOpacity)?ownOpacity:1)*paintOpacity;
  const relativeTop=(box.top-canvas.top)/canvas.height;
  const relativeWidth=box.width/canvas.width;
  const relativeHeight=box.height/canvas.height;
  const lowerFlat=relativeTop>=0.72&&relativeWidth>=0.12&&relativeHeight<=0.075;
  const namedGround=label.includes('ground-shadow')||label.includes('ground_shadow');
  const namedShadow=label.includes('shadow');
  if(namedGround||(lowerFlat&&dark&&(namedShadow||opacity<=0.65))){
    el.style.setProperty('display','none','important');
  }
});
});</script>"""
    seek = (
        "<script>addEventListener('DOMContentLoaded',function(){"
        "document.getAnimations().forEach(function(a){a.pause();a.currentTime=__T__;});"
        "});</script>"
    ).replace("__T__", repr(float(time_ms)))
    css = (
        "html,body{margin:0;padding:0;overflow:hidden;background:%s}"
        "svg{width:%dpx;height:%dpx}" % (bg, viewport, viewport)
    )
    return (
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        + css
        + "</style></head><body>"
        + svg_text
        + shadow_hider
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
            "--disable-dev-shm-usage",
            "--no-first-run", "--no-default-browser-check",
            "--force-device-scale-factor=1",
            "--run-all-compositor-stages-before-draw",
            f"--virtual-time-budget={_VIRTUAL_TIME_MS}",
            f"--window-size={viewport},{viewport}",
            f"--screenshot={png_path}", html_path.resolve().as_uri(),
        ]
        if os.environ.get("CHROME_NO_SANDBOX") == "1":
            # Intended only inside the already-isolated, non-root Docker container.
            cmd.insert(1, "--no-sandbox")
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
