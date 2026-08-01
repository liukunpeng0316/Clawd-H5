from __future__ import annotations

import re
from xml.etree import ElementTree as ET


MAX_SVG_BYTES = 240_000
ALLOWED_TAGS = {
    "svg", "g", "defs", "style", "rect", "circle", "ellipse", "line",
    "path", "polygon", "polyline", "text", "tspan", "clipPath", "mask",
    "linearGradient", "radialGradient", "stop", "use", "title", "desc",
}
DENIED_TEXT = re.compile(
    r"(?:javascript:|data:|(?:https?|file):|@import|expression\s*\(|-moz-binding)",
    re.IGNORECASE,
)


class UnsafeSVG(ValueError):
    pass


def _local_name(value: str) -> str:
    return value.rsplit("}", 1)[-1]


def extract_svg(text: str) -> str:
    """Extract a single SVG document from a model response."""
    match = re.search(r"<svg\b[\s\S]*?</svg>", text, re.IGNORECASE)
    if not match:
        raise UnsafeSVG("模型没有返回完整 SVG")
    svg = match.group(0).strip()
    if len(svg.encode("utf-8")) > MAX_SVG_BYTES:
        raise UnsafeSVG("SVG 体积超过安全上限")
    return svg


def sanitize_svg(svg: str) -> str:
    """Reject active/external SVG content and return normalized XML."""
    try:
        root = ET.fromstring(svg)
    except ET.ParseError as exc:
        raise UnsafeSVG(f"SVG XML 无法解析：{exc}") from exc
    if _local_name(root.tag) != "svg":
        raise UnsafeSVG("根节点不是 SVG")

    for node in root.iter():
        tag = _local_name(node.tag)
        if tag not in ALLOWED_TAGS:
            raise UnsafeSVG(f"SVG 包含不允许的元素：{tag}")
        for raw_name, value in list(node.attrib.items()):
            name = _local_name(raw_name).lower()
            lowered = value.strip().lower()
            if name.startswith("on"):
                raise UnsafeSVG("SVG 包含事件处理器")
            if name in {"href", "src"} and lowered and not lowered.startswith("#"):
                raise UnsafeSVG("SVG 包含外部引用")
            if DENIED_TEXT.search(value):
                raise UnsafeSVG("SVG 属性包含不安全内容")
        if tag == "style" and node.text and DENIED_TEXT.search(node.text):
            raise UnsafeSVG("SVG 样式包含外部资源或可执行内容")

    if not root.tag.startswith("{"):
        root.set("xmlns", "http://www.w3.org/2000/svg")
    else:
        ET.register_namespace("", "http://www.w3.org/2000/svg")
    root.set("width", "500")
    root.set("height", "500")
    root.set("viewBox", root.attrib.get("viewBox", "-15 -25 45 45"))
    return ET.tostring(root, encoding="unicode")
