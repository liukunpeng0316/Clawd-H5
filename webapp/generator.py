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


REFERENCE_HINTS: tuple[tuple[int, str, tuple[str, ...]], ...] = (
    (500, "clawd-salute", ("挥手", "招手", "打招呼", "敬礼", "wave", "salute", "hello")),
    (500, "clawd-clapping", ("鼓掌", "拍手", "clap", "applause")),
    (500, "clawd-coffee", ("咖啡", "coffee")),
    (500, "clawd-running", ("跑步", "奔跑", "逃跑", "running", "run")),
    (500, "clawd-kick-football", ("踢球", "足球", "football", "soccer")),
    (500, "clawd-kick-messi", ("梅西", "messi")),
    (500, "clawd-punching", ("出拳", "拳击", "打拳", "punch", "boxing")),
    (500, "clawd-high-jump", ("跳高", "起跳", "high jump")),
    (500, "clawd-charge", ("冲锋", "冲刺", "charge", "sprint")),
    (500, "clawd-bow-thanks", ("鞠躬", "感谢", "谢谢", "thanks", "thank you", "bow")),
    (500, "clawd-flying-kiss", ("飞吻", "亲亲", "kiss")),
    (500, "clawd-heart", ("爱心", "比心", "heart", "love")),
    (500, "clawd-note-taking", ("记笔记", "记录", "note-taking", "take notes")),
    (500, "clawd-coding", ("写代码", "编程", "代码", "coding", "programming")),
    (500, "clawd-typing", ("打字", "键盘", "typing", "keyboard")),
    (500, "clawd-working-debugger", ("调试", "修bug", "debug", "bug")),
    (500, "clawd-working-building", ("搭建", "建造", "building", "build")),
    (500, "clawd-working-sweeping", ("扫地", "打扫", "sweeping", "cleaning")),
    (500, "clawd-working-juggling", ("杂耍", "抛球", "juggling")),
    (500, "clawd-working-wizard", ("魔法", "法师", "wizard", "magic")),
    (500, "clawd-lion-dance", ("舞狮", "lion dance")),
    (500, "clawd-snake-charmer", ("耍蛇", "吹笛", "snake charmer")),
    (500, "clawd-money-bag", ("钱袋", "发财", "赚钱", "money", "rich")),
    (400, "clawd-go-sleep", ("睡觉", "晚安", "入睡", "sleep", "good night")),
    (400, "clawd-drowsy", ("困了", "犯困", "打瞌睡", "drowsy", "sleepy")),
    (400, "clawd-thinking-frozen", ("思考", "想一想", "沉思", "thinking", "think")),
    (400, "clawd-idle-living", ("发呆", "无聊", "待机", "idle", "bored")),
    (400, "clawd-crying", ("哭泣", "流泪", "伤心", "crying", "sad")),
    (400, "clawd-furious", ("愤怒", "生气", "暴怒", "furious", "angry")),
    (400, "clawd-panic", ("惊慌", "慌张", "panic")),
    (400, "clawd-confused-big-question", ("困惑", "疑问", "不明白", "confused", "question")),
    (400, "clawd-pleading", ("恳求", "求求", "拜托", "pleading", "beg")),
    (400, "clawd-sick", ("生病", "难受", "发烧", "sick", "ill")),
    (400, "clawd-surprised", ("惊讶", "震惊", "surprised", "shocked")),
    (400, "clawd-wow", ("哇", "wow", "amazed")),
    (400, "clawd-rofl", ("笑翻", "大笑", "笑死", "rofl", "laugh")),
    (400, "clawd-surrender-helpless", ("投降", "无助", "认输", "surrender", "helpless")),
    (400, "clawd-disgusted-retreat", ("嫌弃", "后退", "恶心", "disgusted", "retreat")),
    (400, "clawd-gloomy-crawl", ("阴郁", "低落", "爬行", "gloomy", "crawl")),
    (400, "clawd-approved", ("通过", "批准", "同意", "approved", "approve")),
    (400, "clawd-rejected", ("拒绝", "不行", "否决", "rejected", "reject")),
    (400, "clawd-ok-nodding", ("好的", "没问题", "ok", "okay")),
    (400, "clawd-nodding-smile", ("点头", "赞同", "nodding", "nod")),
    (400, "clawd-innocent-blink", ("眨眼", "无辜", "blink", "innocent")),
    (400, "clawd-curious", ("好奇", "探头", "curious")),
    (400, "clawd-broke", ("破产", "没钱", "贫穷", "broke")),
    (300, "clawd-happy", ("开心", "高兴", "快乐", "happy", "joy")),
    (300, "clawd-smile", ("微笑", "smile")),
)


SYSTEM_PROMPT = """You create one safe, self-contained animated SVG of Clawd, a tiny pixel crab.

OUTPUT CONTRACT
- Return exactly one complete `<svg>...</svg>` and nothing else: no Markdown, prose, or code fence.
- Keep it valid XML, compact, and under 12,000 characters.
- Canvas: width="500", height="500", viewBox="-15 -25 45 45", shape-rendering="crispEdges".
- Use only SVG shapes, groups, defs, style, text/tspan, clipPath/mask, gradients, stops, and internal `use` references.
- Never use script, foreignObject, image, iframe, event handlers, JavaScript, data URLs, external links/resources, `@import`, or SMIL animation. Use CSS `@keyframes` only.

CLAWD IDENTITY
- Pixel-art body made primarily from rectangles. Flat body color #DE886D; eyes #000000. No mouth, ever.
- Canonical torso: x=2 y=6 width=11 height=7. Center x is about 7.5.
- Eyes: left x=4 y=8, right x=10 y=8, normally 1x2 black rectangles.
- Arms: left x=0 y=9 size=2x2, right x=13 y=9 size=2x2; keep them visually attached to the torso.
- Legs meet the torso at y=13: x=3,5,9,11, normally 1x2. Standing legs may start at y=12 with overlap.
- Variant poses may squash or stretch the torso, but keep it recognizable: scaleX 0.9-1.18, scaleY 0.7-1.1.

MOTION AND COMPOSITION
- Show one character, one immediately readable main action, and no detailed background scene.
- Prefer pose, eye shape, props, and effects over words. If essential, use only 2-4 floating characters, never a speech bubble.
- Make a seamless loop, normally 1.2-2.0 seconds. The first and last pose must match.
- Use one main motion plus at most two subtle secondary motions such as body bob or blink. Do not stack blink animations.
- Rotate around believable joints; use translate for travel and scale for squash. Any scaled element must set transform-box:fill-box and an explicit transform-origin.
- Check motion extremes: limbs must not detach, props must remain held, eyes must stay on the face, and foreground arms/props must not cover both eyes.
- Layer back to front: optional ground shadow, legs, torso, eyes, rear arm, front arm/prop, small effects.
- Keep all visible content inside roughly a 20-33 viewBox-unit square and within the canvas. Avoid gradients/filters on the body and avoid excessive particles.

Before answering, silently verify complete closing tags, valid CSS, attached limbs, unclipped motion, and a seamless loop. Output only the final SVG."""


def _reference_files(stem: str) -> tuple[Path, Path] | None:
    for collection in ("original", "upstream"):
        root = ROOT / "assets" / collection
        caption = root / "captions" / f"{stem}.md"
        svg = root / "svg" / f"{stem}.svg"
        if caption.exists() and svg.exists():
            return caption, svg
    return None


def select_references(prompt: str, limit: int = 1) -> list[tuple[Path, Path]]:
    normalized = re.sub(r"\s+", " ", prompt.lower()).strip()
    ranked: list[tuple[int, str]] = []
    for priority, stem, keywords in REFERENCE_HINTS:
        matches = [keyword for keyword in keywords if keyword in normalized]
        if matches:
            ranked.append((priority + max(len(item) for item in matches), stem))
    ranked.sort(reverse=True)
    stems = [stem for _, stem in ranked] or ["clawd-static-base"]
    chosen: list[tuple[Path, Path]] = []
    for stem in dict.fromkeys(stems):
        files = _reference_files(stem)
        if files:
            chosen.append(files)
        if len(chosen) >= max(1, limit):
            break
    return chosen


def _compact_reference_svg(svg: str) -> str:
    svg = re.sub(r"<!--[\s\S]*?-->", "", svg)
    return "\n".join(line.strip() for line in svg.splitlines() if line.strip())


def _reference_context(prompt: str) -> str:
    items: list[str] = []
    prefer_chinese = bool(re.search(r"[\u3400-\u9fff]", prompt))
    for caption, svg in select_references(prompt):
        localized = caption.with_name(caption.stem + ".zh.md")
        caption_path = localized if prefer_chinese and localized.exists() else caption
        items.append(
            f"REFERENCE `{svg.stem}` (use as an identity/technique example, not as extra instructions):\n"
            f"{_read(caption_path).strip()}\nREFERENCE SVG:\n{_compact_reference_svg(_read(svg))}"
        )
    return "\n\n".join(items)


def build_messages(prompt: str, previous_svg: str | None, prompts: list[str]) -> list[dict]:
    if previous_svg:
        original = prompts[0] if prompts else prompt
        recent = prompts[1:-1][-3:] if len(prompts) > 2 else []
        recent_text = json.dumps(recent, ensure_ascii=False) if recent else "none"
        user = f"""Revise the existing SVG surgically. Preserve every unrelated shape, color, proportion, and timing.

ORIGINAL REQUEST: {original}
RECENT PRIOR CHANGES: {recent_text}
NEW CHANGE: {prompt}

EXISTING SVG:
{previous_svg}

Return the complete revised SVG, not a patch."""
    else:
        user = f"""Create a looping Clawd sticker for this request:
{prompt}

{_reference_context(prompt)}

Use the reference only to preserve Clawd's identity and learn a relevant motion technique. Follow the user's requested action."""
    return [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user}]


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
        min_units=33.0,
        max_units=45.0,
        max_duration_ms=2000,
    )
    svg_to_gif.export_svg(svg_path, gif_path, options, chrome_render.find_chrome())
