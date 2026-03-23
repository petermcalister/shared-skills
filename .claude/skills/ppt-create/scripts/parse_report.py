#!/usr/bin/env python3
"""Parse a Markdown report into a PowerPoint manifest JSON.

Usage:
    cd .claude/skills/ppt-create/references && uv run python ../scripts/parse_report.py \
        --input report.md --images images/ --archetype executive-briefing --output manifest.json
"""

import argparse
import inspect
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional

import mistune

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# ---------------------------------------------------------------------------
# AST text extraction helpers
# ---------------------------------------------------------------------------

def extract_text(children: list[dict[str, Any]]) -> str:
    """Recursively extract plain text from a list of AST child nodes.

    Args:
        children: List of mistune AST child nodes.

    Returns:
        Concatenated plain text string.
    """
    try:
        parts: list[str] = []
        for child in children:
            if child.get("type") == "text":
                parts.append(child.get("raw", ""))
            elif child.get("type") == "codespan":
                parts.append(child.get("raw", ""))
            elif child.get("type") == "strong":
                parts.append(extract_text(child.get("children", [])))
            elif child.get("type") == "emphasis":
                parts.append(extract_text(child.get("children", [])))
            elif child.get("type") == "link":
                parts.append(extract_text(child.get("children", [])))
            elif "children" in child:
                parts.append(extract_text(child["children"]))
            elif "raw" in child:
                parts.append(child["raw"])
        return "".join(parts)
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"An error occurred in {current_function}: {e}")
        logger.warning(f"An error occurred in {current_function}: {e}")
        raise e


def extract_list_items(list_node: dict[str, Any]) -> list[str]:
    """Extract bullet strings from a mistune list AST node.

    Args:
        list_node: A mistune AST node of type 'list'.

    Returns:
        List of bullet text strings.
    """
    try:
        items: list[str] = []
        for li in list_node.get("children", []):
            if li.get("type") == "list_item":
                text = extract_text(li.get("children", []))
                if text.strip():
                    items.append(text.strip())
        return items
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"An error occurred in {current_function}: {e}")
        logger.warning(f"An error occurred in {current_function}: {e}")
        raise e


def find_image_in_children(children: list[dict[str, Any]]) -> Optional[dict[str, str]]:
    """Find the first image node in a list of AST children.

    Args:
        children: List of mistune AST child nodes.

    Returns:
        Dict with 'url' and 'alt' keys, or None if no image found.
    """
    try:
        for child in children:
            if child.get("type") == "image":
                alt = extract_text(child.get("children", []))
                url = child.get("attrs", {}).get("url", "")
                return {"url": url, "alt": alt}
            if "children" in child:
                result = find_image_in_children(child["children"])
                if result:
                    return result
        return None
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"An error occurred in {current_function}: {e}")
        logger.warning(f"An error occurred in {current_function}: {e}")
        raise e


def extract_metrics_from_paragraph(children: list[dict[str, Any]]) -> list[tuple[str, str]]:
    """Extract bold-colon metric patterns from a paragraph's children.

    Handles both single-metric paragraphs (one **Label:** value) and
    multi-metric paragraphs where multiple metrics are separated by softbreaks
    within one paragraph (common when markdown uses single newlines).

    Args:
        children: List of mistune AST child nodes from a paragraph.

    Returns:
        List of (label, value) tuples. Empty list if no metrics found.
    """
    try:
        if not children:
            return []

        # Split children into segments separated by softbreaks
        segments: list[list[dict[str, Any]]] = []
        current_segment: list[dict[str, Any]] = []
        for child in children:
            if child.get("type") == "softbreak":
                if current_segment:
                    segments.append(current_segment)
                    current_segment = []
            else:
                current_segment.append(child)
        if current_segment:
            segments.append(current_segment)

        # Try to parse each segment as a metric
        metrics: list[tuple[str, str]] = []
        for seg in segments:
            if len(seg) < 2:
                continue
            first = seg[0]
            if first.get("type") != "strong":
                continue
            strong_text = extract_text(first.get("children", []))
            if not strong_text.endswith(":"):
                continue
            label = strong_text.rstrip(":").strip()
            value = extract_text(seg[1:]).strip()
            if label and value:
                metrics.append((label, value))

        return metrics
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"An error occurred in {current_function}: {e}")
        logger.warning(f"An error occurred in {current_function}: {e}")
        raise e


# ---------------------------------------------------------------------------
# Image resolution
# ---------------------------------------------------------------------------

def resolve_image_path(image_url: str, images_dir: Optional[str]) -> str:
    """Resolve an image URL to an actual file path.

    Checks the images directory for a matching filename if the URL is not
    already a valid path.

    Args:
        image_url: The image URL/path from the markdown.
        images_dir: Optional directory to scan for image files.

    Returns:
        Resolved image path string.
    """
    try:
        # If it's already absolute and exists, use it
        if os.path.isabs(image_url) and os.path.exists(image_url):
            return image_url

        # Try the images directory
        if images_dir:
            basename = os.path.basename(image_url)
            candidate = os.path.join(images_dir, basename)
            if os.path.exists(candidate):
                return candidate

            # Try the original relative path from images_dir
            candidate2 = os.path.join(images_dir, image_url)
            if os.path.exists(candidate2):
                return candidate2

        # Return as-is (build_deck will resolve relative to manifest dir)
        return image_url
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"An error occurred in {current_function}: {e}")
        logger.warning(f"An error occurred in {current_function}: {e}")
        raise e


# ---------------------------------------------------------------------------
# Section processor
# ---------------------------------------------------------------------------

def process_section(
    heading_level: int,
    heading_text: str,
    body_tokens: list[dict[str, Any]],
    images_dir: Optional[str],
    is_first_h1: bool,
) -> list[dict[str, Any]]:
    """Convert a heading and its body tokens into slide dicts.

    Args:
        heading_level: The heading level (1, 2, 3).
        heading_text: The heading text.
        body_tokens: List of AST tokens under this heading.
        images_dir: Optional directory for image resolution.
        is_first_h1: Whether this is the first H1 in the document.

    Returns:
        List of slide dict objects for the manifest.
    """
    try:
        slides: list[dict[str, Any]] = []

        # H1 first occurrence -> title slide; subsequent H1 or H2 -> section_header
        if heading_level == 1 and is_first_h1:
            slide: dict[str, Any] = {"type": "title", "title": heading_text}
            # Check for subtitle in first paragraph
            for token in body_tokens:
                if token.get("type") == "paragraph":
                    text = extract_text(token.get("children", []))
                    if text.strip():
                        slide["subtitle"] = text.strip()
                        break
            slides.append(slide)
            return slides

        if heading_level in (1, 2):
            slides.append({"type": "section_header", "title": heading_text})
            return slides

        # H3 -> content slide, diagram, or metrics depending on body
        paragraphs: list[str] = []
        bullets: list[str] = []
        images: list[dict[str, str]] = []
        metrics: list[dict[str, str]] = []

        for token in body_tokens:
            ttype = token.get("type")

            if ttype == "paragraph":
                children = token.get("children", [])

                # Check for image
                img = find_image_in_children(children)
                if img:
                    resolved = resolve_image_path(img["url"], images_dir)
                    images.append({"url": resolved, "alt": img["alt"]})
                    continue

                # Check for metric pattern(s)
                found_metrics = extract_metrics_from_paragraph(children)
                if found_metrics:
                    for label, value in found_metrics:
                        metrics.append({"label": label, "value": value})
                    continue

                # Regular paragraph
                text = extract_text(children)
                if text.strip():
                    paragraphs.append(text.strip())

            elif ttype == "list":
                bullets.extend(extract_list_items(token))

            elif ttype == "blank_line":
                continue

        # Decide slide type based on content
        if metrics:
            slides.append({
                "type": "metrics",
                "title": heading_text,
                "metrics": [{"label": m["label"], "value": m["value"], "trend": "flat"} for m in metrics],
            })
            return slides

        if images:
            img = images[0]
            if not paragraphs and not bullets:
                # Only an image -> diagram_full
                slides.append({
                    "type": "diagram_full",
                    "title": heading_text,
                    "image_path": img["url"],
                })
            else:
                # Image with text -> diagram with caption
                caption = img["alt"] if img["alt"] else (paragraphs[0] if paragraphs else None)
                slide_d: dict[str, Any] = {
                    "type": "diagram",
                    "title": heading_text,
                    "image_path": img["url"],
                }
                if caption:
                    slide_d["caption"] = caption
                slides.append(slide_d)
            return slides

        # Default: content slide
        body = "\n\n".join(paragraphs) if paragraphs else ""
        slide_c: dict[str, Any] = {"type": "content", "title": heading_text, "body": body}
        if bullets:
            slide_c["bullets"] = bullets
        slides.append(slide_c)
        return slides

    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"An error occurred in {current_function}: {e}")
        logger.warning(f"An error occurred in {current_function}: {e}")
        raise e


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------

def parse_markdown(
    markdown_text: str,
    images_dir: Optional[str] = None,
    archetype: str = "general",
    palette: str = "midnight",
) -> dict[str, Any]:
    """Parse a Markdown report into a PowerPoint manifest dict.

    Splits the markdown into sections by heading, then converts each section
    into one or more slide definitions matching the build_deck.py manifest format.

    Args:
        markdown_text: The raw markdown content.
        images_dir: Optional directory containing images referenced in markdown.
        archetype: Presentation archetype name.
        palette: Colour palette key.

    Returns:
        Complete manifest dict ready for JSON serialisation.
    """
    try:
        md = mistune.create_markdown(renderer=None)
        tokens = md(markdown_text)

        # Split tokens into sections: each heading starts a new section
        sections: list[tuple[int, str, list[dict[str, Any]]]] = []
        current_heading: Optional[tuple[int, str]] = None
        current_body: list[dict[str, Any]] = []

        for token in tokens:
            if token.get("type") == "heading":
                # Flush previous section
                if current_heading is not None:
                    sections.append((current_heading[0], current_heading[1], current_body))
                level = token.get("attrs", {}).get("level", 1)
                text = extract_text(token.get("children", []))
                current_heading = (level, text)
                current_body = []
            else:
                current_body.append(token)

        # Flush last section
        if current_heading is not None:
            sections.append((current_heading[0], current_heading[1], current_body))

        # Process sections into slides
        slides: list[dict[str, Any]] = []
        h1_seen = False

        for level, text, body in sections:
            is_first_h1 = (level == 1 and not h1_seen)
            if level == 1:
                h1_seen = True
            section_slides = process_section(level, text, body, images_dir, is_first_h1)
            slides.extend(section_slides)

        manifest: dict[str, Any] = {
            "archetype": archetype,
            "palette": palette,
            "font_heading": "Georgia",
            "font_body": "Calibri",
            "slides": slides,
        }

        return manifest

    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"An error occurred in {current_function}: {e}")
        logger.warning(f"An error occurred in {current_function}: {e}")
        raise e


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point for parse_report.py.

    Parses command-line arguments and runs the markdown-to-manifest conversion.
    """
    try:
        parser = argparse.ArgumentParser(
            description="Parse a Markdown report into a PowerPoint manifest JSON."
        )
        parser.add_argument("--input", required=True, help="Path to input Markdown file")
        parser.add_argument("--images", default=None, help="Directory containing images")
        parser.add_argument("--archetype", default="general", help="Presentation archetype")
        parser.add_argument("--palette", default="midnight", help="Colour palette key")
        parser.add_argument("--output", required=True, help="Output JSON manifest path")
        args = parser.parse_args()

        input_path = os.path.abspath(args.input)
        output_path = os.path.abspath(args.output)
        images_dir = os.path.abspath(args.images) if args.images else None

        if not os.path.exists(input_path):
            print(f"Error: input file not found: {input_path}")
            sys.exit(1)

        if images_dir and not os.path.isdir(images_dir):
            print(f"Warning: images directory not found: {images_dir}")
            images_dir = None

        with open(input_path, "r", encoding="utf-8") as f:
            markdown_text = f.read()

        manifest = parse_markdown(markdown_text, images_dir, args.archetype, args.palette)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        logger.info("Wrote manifest to %s (%d slides)", output_path, len(manifest["slides"]))

    except SystemExit:
        raise
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"An error occurred in {current_function}: {e}")
        logger.warning(f"An error occurred in {current_function}: {e}")
        raise e


if __name__ == "__main__":
    main()
