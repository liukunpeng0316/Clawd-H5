from __future__ import annotations

import base64
import io
import json
import logging
import os
import re
import sys
from pathlib import Path

import httpx
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import chrome_render  # noqa: E402
import svg_to_gif  # noqa: E402

from webapp.security import extract_svg, sanitize_svg  # noqa: E402


PRIMARY_MODEL = os.getenv("GENERATION_MODEL", "deepseek-v4-flash")
PRIMARY_BASE_URL = os.getenv("GENERATION_BASE_URL", "https://api.deepseek.com").rstrip("/")
FALLBACK_MODEL = os.getenv("STEPFUN_MODEL", "step-3.7-flash")
FALLBACK_BASE_URL = os.getenv("STEPFUN_BASE_URL", "https://api.stepfun.com/step_plan/v1").rstrip("/")
SECONDARY_FALLBACK_BASE_URL = os.getenv("STEPFUN_FALLBACK_BASE_URL", "https://api.stepfun.com/v1").rstrip("/")
TIMEOUT = float(os.getenv("STEPFUN_TIMEOUT", "180"))
log = logging.getLogger("clawd-workshop.generator")


class GenerationError(RuntimeError):
    pass


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _reference_score(prompt: str, caption: str, name: str) -> int:
    compact = re.sub(r"\s+", "", prompt.lower())
    haystack = (caption + name).lower()
    score = 0
    for size in (4, 3, 2):
        for index in range(max(0, len(compact) - size + 1)):
            token = compact[index:index + size]
            if token in haystack:
                score += size * size
    keyword_map = {
        "开心": "happy smile jump", "高兴": "happy smile jump", "哭": "crying sad",
        "困": "drowsy sleep", "睡": "sleep drowsy", "跑": "running", "鼓掌": "clapping",
        "咖啡": "coffee", "思考": "thinking", "困惑": "confused", "生气": "furious",
        "足球": "kick football", "亲": "kiss", "爱": "heart", "代码": "coding typing",
    }
    for key, words in keyword_map.items():
        if key in prompt and any(word in haystack for word in words.split()):
            score += 100
    return score


def select_references(prompt: str, limit: int = 1) -> list[tuple[Path, Path]]:
    ranked: list[tuple[int, Path, Path]] = []
    for caption in ROOT.glob("assets/*/captions/*.md"):
        if caption.name.endswith(".zh.md") or caption.stem == "clawd-body-structure":
            continue
        svg = caption.parent.parent / "svg" / f"{caption.stem}.svg"
        if not svg.exists():
            continue
        text = _read(caption)
        zh = caption.with_name(caption.stem + ".zh.md")
        if zh.exists():
            text += "\n" + _read(zh)
        ranked.append((_reference_score(prompt, text, caption.stem), caption, svg))
    ranked.sort(key=lambda item: (item[0], item[1].name), reverse=True)
    chosen = ranked[:limit]
    if chosen and chosen[0][0] == 0:
        fallbacks = ["clawd-static-base", "clawd-happy", "clawd-thinking-frozen"]
        chosen = []
        for name in fallbacks:
            caption = ROOT / "assets" / ("upstream" if name in {"clawd-static-base", "clawd-happy"} else "original") / "captions" / f"{name}.md"
            svg = caption.parent.parent / "svg" / f"{name}.svg"
            if caption.exists() and svg.exists():
                chosen.append((0, caption, svg))
    return [(caption, svg) for _, caption, svg in chosen]


def build_messages(prompt: str, previous_svg: str | None, prompts: list[str]) -> list[dict]:
    rules = _read(ROOT / ".claude" / "skills" / "any2clawd" / "references" / "rules.md")
    body = _read(ROOT / "assets" / "original" / "captions" / "clawd-body-structure.md")
    references = []
    for caption, svg in select_references(prompt):
        references.append(f"REFERENCE {svg.name}\n{_read(caption)}\nSVG:\n{_read(svg)}")
    system = f"""You generate safe, self-contained animated SVG code for the Clawd pixel crab.
Return exactly one complete <svg>...</svg>, with no Markdown and no explanation.
Keep the SVG compact and under 12,000 characters. Prefer reusable CSS classes and simple shapes.
Never include script, foreignObject, image, iframe, external links, data URLs, event handlers, or remote resources.
Use CSS keyframes only. Keep the standard Clawd identity and follow every rule below.

CORE RULES:
{rules}

BODY SPEC:
{body}
"""
    context = "\n\n".join(references)
    if previous_svg:
        user = f"""Revise the existing animation according to the newest request.
Conversation requests: {json.dumps(prompts, ensure_ascii=False)}
Newest request: {prompt}

EXISTING SVG:
{previous_svg}

Relevant references:
{context}
"""
    else:
        user = f"""Create a single-character looping Clawd sticker animation for this request:
{prompt}

Relevant references:
{context}
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


async def _chat(messages: list[dict], max_tokens: int = 10000) -> str:
    providers = [
        (
            "DeepSeek",
            PRIMARY_BASE_URL,
            PRIMARY_MODEL,
            os.getenv("DEEPSEEK_API_KEY", "").strip(),
            {"thinking": {"type": "disabled"}},
        ),
        (
            "StepFun Plan",
            FALLBACK_BASE_URL,
            FALLBACK_MODEL,
            os.getenv("STEPFUN_API_KEY", "").strip(),
            {},
        ),
        (
            "StepFun fallback",
            SECONDARY_FALLBACK_BASE_URL,
            FALLBACK_MODEL,
            os.getenv("STEPFUN_API_KEY", "").strip(),
            {},
        ),
    ]
    failures: list[str] = []
    response = None
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        for label, endpoint, model, api_key, extra in providers:
            if not api_key:
                failures.append(f"{label}: API Key 未配置")
                continue
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.2,
                "max_tokens": max_tokens,
                **extra,
            }
            try:
                candidate = await client.post(
                    f"{endpoint}/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json=payload,
                )
                if candidate.status_code < 400:
                    response = candidate
                    break
                log.warning("%s returned HTTP %s; trying fallback", label, candidate.status_code)
                failures.append(f"{label}: HTTP {candidate.status_code}")
            except httpx.HTTPError as exc:
                log.warning("%s failed with %s; trying fallback", label, type(exc).__name__)
                failures.append(f"{label}: {type(exc).__name__}")
    if response is None:
        raise GenerationError("主模型和备用模型均失败：" + " | ".join(failures))
    data = response.json()
    try:
        choice = data["choices"][0]
        content = choice["message"]["content"]
        log.info("Model response chars=%s finish_reason=%s", len(content), choice.get("finish_reason", "unknown"))
        return content
    except (KeyError, IndexError, TypeError) as exc:
        raise GenerationError("模型 API 返回格式异常") from exc


async def generate_svg(prompt: str, previous_svg: str | None, prompts: list[str]) -> str:
    response = await _chat(build_messages(prompt, previous_svg, prompts))
    return sanitize_svg(extract_svg(response))


def render_review_image(svg: str) -> bytes:
    duration = svg_to_gif.parse_duration_ms(svg)
    times = [0, duration * 0.4, duration * 0.8]
    frames = chrome_render.render_frames(
        svg, times, viewport=360, background="white", workers=1, timeout=25
    )
    sheet = Image.new("RGB", (360 * len(frames), 360), "white")
    for index, frame in enumerate(frames):
        sheet.paste(frame.convert("RGB"), (index * 360, 0))
    output = io.BytesIO()
    sheet.save(output, format="PNG", optimize=True)
    return output.getvalue()


async def review_and_maybe_fix(svg: str, prompt: str, png: bytes) -> str:
    image_url = "data:image/png;base64," + base64.b64encode(png).decode("ascii")
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": f"""Inspect these three sampled frames of an animated Clawd sticker requested as: {prompt}
Check only obvious defects: blank output, clipping, detached limbs, unreadable pose, broken prop placement.
If acceptable, answer exactly OK.
If a defect is obvious, return one complete corrected SVG and nothing else.

CURRENT SVG:
{svg}"""},
            {"type": "image_url", "image_url": {"url": image_url}},
        ],
    }]
    try:
        response = (await _chat(messages, max_tokens=16000)).strip()
        if response.upper() == "OK" or "<svg" not in response.lower():
            return svg
        return sanitize_svg(extract_svg(response))
    except Exception:
        return svg


def export_gif(svg_path: Path, gif_path: Path) -> None:
    options = svg_to_gif.ExportOptions(
        size=240,
        fps=15,
        padding=6,
        alpha_threshold=128,
        background="transparent",
        hide_ground_shadow=True,
        workers=1,
        timeout=25,
        min_units=20.0,
        max_units=33.0,
        max_duration_ms=2000,
    )
    svg_to_gif.export_svg(svg_path, gif_path, options, chrome_render.find_chrome())
