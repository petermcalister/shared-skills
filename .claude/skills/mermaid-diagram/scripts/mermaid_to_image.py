#!/usr/bin/env python3
"""Convert Mermaid diagrams to PNG/SVG images.

Renders .mmd files via mermaid-cli (mmdc). Supports single files, batch
conversion, stdin input, and theme customization.

Usage:
    python mermaid_to_image.py diagram.mmd output.png
    python mermaid_to_image.py diagram.mmd output.svg --theme dark
    python mermaid_to_image.py diagrams/ output/ --format png --recursive
    echo "graph TD; A-->B" | python mermaid_to_image.py - output.png

Requirements:
    mermaid-cli: npm install -g @mermaid-js/mermaid-cli
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

_USE_SHELL = sys.platform == "win32"
VALID_THEMES = ["default", "forest", "dark", "neutral", "base"]
VALID_FORMATS = ["png", "svg", "pdf"]


class MermaidRenderer:
    """Render Mermaid diagrams to images using mermaid-cli."""

    def __init__(
        self,
        theme: str = "default",
        background: str = "transparent",
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale: int = 1,
    ):
        if not self._check_mmdc():
            print("ERROR: mmdc not found. Install: npm install -g @mermaid-js/mermaid-cli", file=sys.stderr)
            sys.exit(1)
        self.theme = theme if theme in VALID_THEMES else "default"
        self.background = background
        self.width = width
        self.height = height
        self.scale = max(1, min(3, scale))

    @staticmethod
    def _check_mmdc() -> bool:
        try:
            subprocess.run(["mmdc", "--version"], capture_output=True, timeout=10, shell=_USE_SHELL)
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def render(self, input_path: Path, output_path: Path) -> bool:
        cmd = ["mmdc", "-i", str(input_path), "-o", str(output_path)]
        cmd.extend(["-t", self.theme, "-b", self.background])
        if self.width:
            cmd.extend(["-w", str(self.width)])
        if self.height:
            cmd.extend(["-H", str(self.height)])
        if self.scale != 1:
            cmd.extend(["-s", str(self.scale)])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, shell=_USE_SHELL)
            if result.returncode != 0:
                print(f"ERROR: {result.stderr}", file=sys.stderr)
                return False
            if not output_path.exists() or output_path.stat().st_size == 0:
                print(f"ERROR: No output: {output_path}", file=sys.stderr)
                return False
            return True
        except subprocess.TimeoutExpired:
            print("ERROR: Render timed out (60s)", file=sys.stderr)
            return False
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return False

    def render_from_string(self, mermaid_code: str, output_path: Path) -> bool:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False) as f:
            f.write(mermaid_code)
            temp_path = Path(f.name)
        try:
            return self.render(temp_path, output_path)
        finally:
            temp_path.unlink(missing_ok=True)

    def batch_render(self, input_dir: Path, output_dir: Path, fmt: str = "png", recursive: bool = False) -> dict:
        output_dir.mkdir(parents=True, exist_ok=True)
        pattern = "**/*.mmd" if recursive else "*.mmd"
        results = {"success": 0, "failed": 0, "files": []}
        for mmd_file in sorted(input_dir.glob(pattern)):
            out_file = output_dir / mmd_file.with_suffix(f".{fmt}").name
            ok = self.render(mmd_file, out_file)
            results["success" if ok else "failed"] += 1
            results["files"].append({"input": str(mmd_file), "output": str(out_file), "ok": ok})
            print(f"  {'✅' if ok else '❌'} {mmd_file.name}")
        return results


def main():
    parser = argparse.ArgumentParser(description="Convert Mermaid diagrams to images")
    parser.add_argument("input", help="Input .mmd file, directory, or '-' for stdin")
    parser.add_argument("output", help="Output file or directory")
    parser.add_argument("--format", default="png", choices=VALID_FORMATS, help="Output format")
    parser.add_argument("--theme", default="default", choices=VALID_THEMES, help="Mermaid theme")
    parser.add_argument("--background", default="transparent", help="Background color")
    parser.add_argument("--width", type=int, default=None, help="Output width in pixels")
    parser.add_argument("--height", type=int, default=None, help="Output height in pixels")
    parser.add_argument("--scale", type=int, default=1, help="Scale factor (1-3)")
    parser.add_argument("--recursive", action="store_true", help="Process subdirectories")
    args = parser.parse_args()

    renderer = MermaidRenderer(args.theme, args.background, args.width, args.height, args.scale)

    if args.input == "-":
        code = sys.stdin.read()
        ok = renderer.render_from_string(code, Path(args.output))
        sys.exit(0 if ok else 1)

    input_path = Path(args.input)
    if input_path.is_dir():
        results = renderer.batch_render(input_path, Path(args.output), args.format, args.recursive)
        print(f"\nBatch: {results['success']} ok, {results['failed']} failed")
        sys.exit(1 if results["failed"] else 0)
    else:
        ok = renderer.render(input_path, Path(args.output))
        if ok:
            print(args.output)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
