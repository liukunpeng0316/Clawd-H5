#!/usr/bin/env python3
"""Promote workspace SVG animations into the reference knowledge base.

Usage:
    python promote_svg.py --list              # List un-promoted SVGs
    python promote_svg.py --promote NAME      # Promote a single SVG (e.g. clawd-charge)
    python promote_svg.py --promote-all       # Promote all un-promoted SVGs (templates only)
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
# Downstream development workspace: new SVGs are authored here (gitignored), then
# promoted into a named collection under assets/<collection>/.
WORKSPACE = ROOT / "workspace"
# Read-only reference collections never written to by promotion.
READONLY_COLLECTIONS = {"upstream", "original"}
# Where the chosen collection name is remembered (gitignored, per-checkout).
COLLECTION_CONFIG = ROOT / ".collection"
DEFAULT_COLLECTION = "generated"


def resolve_collection(name: str | None) -> str:
    """Pick the target collection: --collection > .collection file > prompt."""
    if name:
        chosen = name.strip()
    elif COLLECTION_CONFIG.exists():
        chosen = COLLECTION_CONFIG.read_text(encoding="utf-8").strip()
    else:
        try:
            entered = input(
                "Name your emoji collection (when building a public knowledge base, "
                "using your username is recommended) "
                f"[default {DEFAULT_COLLECTION}]: "
            ).strip()
        except EOFError:
            entered = ""
        chosen = entered or DEFAULT_COLLECTION
        COLLECTION_CONFIG.write_text(chosen + "\n", encoding="utf-8")
        print(f"✅ Remembered collection name: {chosen} (stored in .collection; change it anytime or override with --collection)")
    if chosen in READONLY_COLLECTIONS:
        raise SystemExit(f"❌ '{chosen}' is a read-only reference library; please choose a different collection name")
    return chosen


def collection_dirs(collection: str) -> tuple[Path, Path]:
    svg_dir = ASSETS / collection / "svg"
    captions_dir = ASSETS / collection / "captions"
    svg_dir.mkdir(parents=True, exist_ok=True)
    captions_dir.mkdir(parents=True, exist_ok=True)
    return svg_dir, captions_dir


def ref_svg_dirs() -> list[Path]:
    """All existing collection svg dirs, used to avoid promoting a duplicate name."""
    return sorted(p for p in ASSETS.glob("*/svg") if p.is_dir())

# Standard body parts from clawd-body-structure.md
STANDARD_BODY = {
    "torso":     {"x": 2, "y": 6,  "w": 11, "h": 7},
    "left-eye":  {"x": 4, "y": 8,  "w": 1,  "h": 2},
    "right-eye": {"x": 10,"y": 8,  "w": 1,  "h": 2},
    "left-arm":  {"x": 0, "y": 9,  "w": 2,  "h": 2},
    "right-arm": {"x": 13,"y": 9,  "w": 2,  "h": 2},
    "shadow":    {"x": 3, "y": 15, "w": 9,  "h": 1},
}
SHAPE_TAGS = {"rect", "circle", "ellipse", "line", "path", "polygon", "polyline", "text", "use"}
BODY_COLOR = "#DE886D"
EYE_COLOR = "#000000"


def local_name(tag: str) -> str:
    """Return an XML tag or attribute name without its namespace."""
    return tag.rsplit("}", 1)[-1]


def clean_attrs(attrs: dict[str, str]) -> dict[str, str]:
    return {local_name(key): value for key, value in attrs.items()}


def parse_opacity(value: str | None) -> float:
    if value in (None, ""):
        return 1.0
    try:
        return float(value)
    except ValueError:
        return 1.0


def is_nonstandard_element(tag: str, attrs: dict[str, str]) -> bool:
    if tag != "rect":
        return True

    fill = attrs.get("fill", "")
    if fill in ("", "none", BODY_COLOR, EYE_COLOR):
        return False

    if fill == EYE_COLOR and parse_opacity(attrs.get("opacity")) < 1:
        return False

    return True


def describe_element(element: dict[str, str]) -> str:
    tag = element.get("tag", "?")
    parts = [tag]
    for key in ("id", "class", "fill", "stroke", "href", "x", "y", "width", "height", "points", "d"):
        value = element.get(key)
        if not value:
            continue
        if key in {"points", "d"} and len(value) > 36:
            value = value[:33] + "..."
        parts.append(f"{key}={value}")
    if element.get("text"):
        parts.append(f"text={element['text']}")
    return " ".join(parts)


def get_unpromoted() -> list[str]:
    """Return SVG basenames in the workspace but not yet in any asset collection."""
    gen_svgs = {p.stem for p in WORKSPACE.glob("*.svg")}
    ref_svgs: set[str] = set()
    for ref_dir in ref_svg_dirs():
        ref_svgs |= {p.stem for p in ref_dir.glob("*.svg")}
    return sorted(gen_svgs - ref_svgs)


def parse_svg(svg_path: Path) -> dict:
    """Extract structural info from an SVG file."""
    content = svg_path.read_text(encoding="utf-8")
    info = {
        "file": svg_path.name,
        "comments": [],
        "keyframes": [],
        "classes": [],
        "rects": [],
        "elements": [],
        "props": [],
        "tag_counts": {},
    }

    # Extract CSS comments
    for m in re.finditer(r'/\*(.+?)\*/', content, re.DOTALL):
        text = m.group(1).strip()
        if len(text) > 3:
            info["comments"].append(text)

    # Extract @keyframes
    for m in re.finditer(r'@keyframes\s+([\w-]+)\s*\{(.+?)\n\s*\}', content, re.DOTALL):
        name = m.group(1)
        body = m.group(2).strip()
        info["keyframes"].append({"name": name, "body": body})

    # Extract animation declarations (class -> animation property)
    for m in re.finditer(r'\.([\w-]+)\s*\{[^}]*animation:\s*([^;]+);', content, re.DOTALL):
        cls = m.group(1)
        anim = m.group(2).strip()
        info["classes"].append({"class": cls, "animation": anim})

    # Extract static transforms
    for m in re.finditer(r'\.([\w-]+)\s*\{[^}]*transform:\s*([^;]+);', content, re.DOTALL):
        cls = m.group(1)
        tf = m.group(2).strip()
        if "animation" not in cls:
            info["classes"].append({"class": cls, "transform": tf})

    root = ET.fromstring(content)
    for node in root.iter():
        tag = local_name(node.tag)
        if tag not in SHAPE_TAGS:
            continue

        attrs = clean_attrs(node.attrib)
        element = {"tag": tag, **attrs}
        if tag == "text" and node.text and node.text.strip():
            element["text"] = node.text.strip()

        info["elements"].append(element)
        info["tag_counts"][tag] = info["tag_counts"].get(tag, 0) + 1

        if tag == "rect":
            info["rects"].append(attrs)

        if is_nonstandard_element(tag, attrs):
            info["props"].append(element)

    return info


def format_analysis(info: dict) -> str:
    """Format parsed SVG info for display."""
    lines = []
    lines.append(f"=== {info['file']} structure analysis ===\n")

    if info["comments"]:
        lines.append("📝 CSS comments:")
        for c in info["comments"]:
            lines.append(f"  {c[:120]}")
        lines.append("")

    if info["keyframes"]:
        lines.append(f"🎬 @keyframes ({len(info['keyframes'])}):")
        for kf in info["keyframes"]:
            # Summarize keyframe
            body_lines = kf["body"].split("\n")
            summary = body_lines[0].strip() if body_lines else ""
            lines.append(f"  - {kf['name']}: {summary} ...")
        lines.append("")

    if info["classes"]:
        lines.append("🎨 Animation/transform classes:")
        for c in info["classes"]:
            if "animation" in c:
                lines.append(f"  .{c['class']} → animation: {c['animation']}")
            if "transform" in c:
                lines.append(f"  .{c['class']} → transform: {c['transform']}")
        lines.append("")

    if info["tag_counts"]:
        counts = ", ".join(f"{tag}={count}" for tag, count in sorted(info["tag_counts"].items()))
        lines.append(f"🧱 SVG elements: {counts}")
        lines.append("")

    if info["props"]:
        lines.append(f"🔧 Props/non-standard elements ({len(info['props'])}):")
        for p in info["props"]:
            lines.append(f"  {describe_element(p)}")
        lines.append("")

    lines.append(f"📐 Total elements: {len(info['elements'])} (rect: {len(info['rects'])})")
    return "\n".join(lines)


def generate_caption_template(name: str, info: dict) -> str:
    """Generate a caption markdown template with parsed animation data."""
    # Collect keyframe summaries
    anim_lines = []
    for kf in info["keyframes"]:
        anim_lines.append(f"- **{kf['name']}**: {{TODO: description}}")

    # Collect animation class info
    for c in info["classes"]:
        if "animation" in c:
            anim_lines.append(f"  - .{c['class']}: {c['animation']}")

    anim_section = "\n".join(anim_lines) if anim_lines else "- {TODO}"

    parts = [
        f"# {name}.svg",
        "",
        "{TODO: one-line description}",
        "",
        "## Body",
        "{TODO: body structure description}",
    ]
    if info["props"]:
        parts.append("")
        parts.append("## Props")
        for p in info["props"]:
            parts.append(f"- {describe_element(p)} {{TODO: name}}")
    parts.extend([
        "",
        "## Animation",
        anim_section,
        "",
        "## Expression",
        "{TODO: expression description}",
        "",
    ])
    template = "\n".join(parts)
    return template


def promote(name: str, svg_dir: Path, captions_dir: Path, dry_run: bool = False):
    """Promote one SVG into assets/<collection>/svg/ and create a caption template."""
    # Normalize name
    if name.endswith(".svg"):
        name = name[:-4]

    src = WORKSPACE / f"{name}.svg"
    if not src.exists():
        print(f"❌ Not found: {src}")
        return False

    dst_svg = svg_dir / f"{name}.svg"
    dst_caption = captions_dir / f"{name}.md"

    if dst_svg.exists():
        print(f"⚠️  {dst_svg.name} already exists in {svg_dir.relative_to(ROOT)}/, skipping copy")
    if dst_caption.exists():
        print(f"⚠️  {dst_caption.name} already exists in {captions_dir.relative_to(ROOT)}/, skipping creation")

    # Parse and display analysis
    info = parse_svg(src)
    print(format_analysis(info))

    if dry_run:
        print("(dry-run mode, no file operations performed)")
        return True

    # Copy SVG
    if not dst_svg.exists():
        shutil.copy2(src, dst_svg)
        print(f"✅ Copied → {dst_svg.relative_to(ROOT)}")

    # Create caption template
    if not dst_caption.exists():
        template = generate_caption_template(name, info)
        dst_caption.write_text(template, encoding="utf-8")
        print(f"✅ Created caption template → {dst_caption.relative_to(ROOT)}")
        print("📝 Please use Claude Code to fill in the {TODO} sections")

    return True


def main():
    parser = argparse.ArgumentParser(description="Promote workspace/ SVGs into your emoji collection")
    parser.add_argument("--list", action="store_true", help="List un-promoted SVGs")
    parser.add_argument("--promote", type=str, metavar="NAME", help="Promote a specific SVG (e.g. clawd-charge)")
    parser.add_argument("--promote-all", action="store_true", help="Create templates for all un-promoted SVGs")
    parser.add_argument("--collection", type=str, metavar="NAME",
                        help="Target collection name assets/<NAME>/ (defaults to reading .collection, or prompts on first run)")
    parser.add_argument("--dry-run", action="store_true", help="Analyze only, do not perform file operations")
    args = parser.parse_args()

    if args.list:
        unpromoted = get_unpromoted()
        if unpromoted:
            print(f"📋 SVGs to promote ({len(unpromoted)}):\n")
            for name in unpromoted:
                print(f"  - {name}")
        else:
            print("✅ All workspace SVGs have been promoted")
        return

    if args.promote or args.promote_all:
        collection = resolve_collection(args.collection)
        svg_dir, captions_dir = collection_dirs(collection)
        print(f"📂 Promotion target collection: assets/{collection}/\n")

    if args.promote:
        promote(args.promote, svg_dir, captions_dir, dry_run=args.dry_run)
        return

    if args.promote_all:
        unpromoted = get_unpromoted()
        if not unpromoted:
            print("✅ All workspace SVGs have been promoted")
            return
        print(f"Promoting {len(unpromoted)} SVGs in batch...\n")
        for name in unpromoted:
            print(f"\n{'='*50}")
            promote(name, svg_dir, captions_dir, dry_run=args.dry_run)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
