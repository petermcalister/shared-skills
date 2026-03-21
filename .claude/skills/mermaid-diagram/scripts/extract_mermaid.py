#!/usr/bin/env python3
"""Extract Mermaid diagrams from Markdown files.

Finds all Mermaid code blocks in Markdown files and can:
1. Extract them to separate .mmd files
2. Validate syntax by attempting to render via mmdc
3. Replace them with image references
4. List all diagrams with metadata

Usage:
    python extract_mermaid.py document.md --output-dir diagrams/
    python extract_mermaid.py document.md --list-only
    python extract_mermaid.py document.md --validate
    python extract_mermaid.py document.md --replace-with-images --image-format png

Requirements:
    For validation: mermaid-cli (npm install -g @mermaid-js/mermaid-cli)
"""

import argparse
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

_USE_SHELL = sys.platform == "win32"


class MermaidDiagram:
    """Represents a single Mermaid diagram extracted from Markdown."""

    def __init__(self, content: str, line_number: int, index: int):
        self.content = content.strip()
        self.line_number = line_number
        self.index = index
        self.hash = hashlib.md5(content.encode()).hexdigest()[:8]

    def get_filename(self, prefix: str = "diagram", extension: str = "mmd") -> str:
        return f"{prefix}-{self.index:03d}-{self.hash}.{extension}"

    def get_first_line(self, max_length: int = 50) -> str:
        first_line = self.content.split("\n")[0].strip()
        return first_line[:max_length] + "..." if len(first_line) > max_length else first_line


class MermaidExtractor:
    """Extract and process Mermaid diagrams from Markdown files."""

    MERMAID_PATTERN = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL | re.MULTILINE)

    def __init__(self, markdown_file: Path):
        self.markdown_file = markdown_file
        self.content = markdown_file.read_text(encoding="utf-8")
        self.diagrams: list[MermaidDiagram] = []
        self._extract_diagrams()

    def _extract_diagrams(self):
        for index, match in enumerate(self.MERMAID_PATTERN.finditer(self.content), start=1):
            lines_before = self.content[: match.start()].count("\n")
            self.diagrams.append(MermaidDiagram(match.group(1), lines_before + 1, index))

    def save_diagrams(self, output_dir: Path, prefix: str = "diagram") -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        saved = []
        for diagram in self.diagrams:
            path = output_dir / diagram.get_filename(prefix=prefix)
            path.write_text(diagram.content, encoding="utf-8")
            print(f"  ✓ Saved: {path}")
            saved.append(path)
        return saved

    def list_diagrams(self):
        if not self.diagrams:
            print("No Mermaid diagrams found.")
            return
        print(f"\nFound {len(self.diagrams)} Mermaid diagram(s) in {self.markdown_file}:\n")
        for d in self.diagrams:
            print(f"  #{d.index} (Line {d.line_number}):")
            print(f"    First line: {d.get_first_line()}")
            print(f"    Hash: {d.hash}")
            print(f"    Lines: {len(d.content.splitlines())}\n")

    def validate_diagrams(self) -> dict[int, Optional[str]]:
        if not _check_mmdc():
            print("ERROR: mmdc not found. Install: npm install -g @mermaid-js/mermaid-cli", file=sys.stderr)
            sys.exit(1)

        results = {}
        print(f"\nValidating {len(self.diagrams)} diagram(s)...\n")
        for d in self.diagrams:
            print(f"  Validating #{d.index}...", end=" ")
            error = self._validate_single(d)
            results[d.index] = error
            print("❌ FAILED" if error else "✅ OK")
            if error:
                print(f"    Error: {error}")

        failed = sum(1 for e in results.values() if e)
        print(f"\nValidation: {len(self.diagrams) - failed}/{len(self.diagrams)} passed")
        return results

    def _validate_single(self, diagram: MermaidDiagram) -> Optional[str]:
        with tempfile.TemporaryDirectory() as tmpdir:
            infile = Path(tmpdir) / f"diagram-{diagram.index}.mmd"
            outfile = Path(tmpdir) / f"diagram-{diagram.index}.svg"
            infile.write_text(diagram.content, encoding="utf-8")
            try:
                result = subprocess.run(
                    ["mmdc", "-i", str(infile), "-o", str(outfile), "-b", "transparent"],
                    capture_output=True, text=True, timeout=30, shell=_USE_SHELL,
                )
                if result.returncode != 0:
                    return result.stderr.strip() or "Unknown rendering error"
                if not outfile.exists() or outfile.stat().st_size == 0:
                    return "Rendering produced no output"
                return None
            except subprocess.TimeoutExpired:
                return "Rendering timed out (30s)"
            except Exception as e:
                return str(e)

    def replace_with_images(self, image_format: str = "png", image_dir: str = "diagrams") -> str:
        modified = self.content
        for d in reversed(self.diagrams):
            img_name = d.get_filename(extension=image_format)
            img_ref = f"![Diagram {d.index}]({image_dir}/{img_name})"
            pattern = re.compile(re.escape(f"```mermaid\n{d.content}\n```"))
            modified = pattern.sub(img_ref, modified, count=1)
        return modified


def _check_mmdc() -> bool:
    try:
        subprocess.run(["mmdc", "--version"], capture_output=True, timeout=10, shell=_USE_SHELL)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def main():
    parser = argparse.ArgumentParser(description="Extract Mermaid diagrams from Markdown")
    parser.add_argument("file", type=Path, help="Markdown file to process")
    parser.add_argument("--output-dir", type=Path, default=None, help="Save .mmd files to directory")
    parser.add_argument("--list-only", action="store_true", help="List diagrams without extracting")
    parser.add_argument("--validate", action="store_true", help="Validate diagrams via mmdc")
    parser.add_argument("--replace-with-images", action="store_true", help="Replace code blocks with image refs")
    parser.add_argument("--image-format", default="png", choices=["png", "svg"], help="Image format")
    parser.add_argument("--prefix", default="diagram", help="Filename prefix")
    args = parser.parse_args()

    if not args.file.exists():
        print(f"Error: {args.file} not found", file=sys.stderr)
        sys.exit(1)

    extractor = MermaidExtractor(args.file)

    if args.list_only:
        extractor.list_diagrams()
    elif args.validate:
        results = extractor.validate_diagrams()
        sys.exit(1 if any(results.values()) else 0)
    elif args.replace_with_images:
        modified = extractor.replace_with_images(args.image_format, args.output_dir or "diagrams")
        print(modified)
    elif args.output_dir:
        extractor.save_diagrams(args.output_dir, args.prefix)
    else:
        extractor.list_diagrams()


if __name__ == "__main__":
    main()
