#!/usr/bin/env python3
"""Resilient Mermaid validation workflow.

Validates Mermaid diagrams with error recovery. Saves .mmd and renders
images with structured error output for agent-driven fix loops.

Usage:
    python validate_mermaid.py --code "flowchart TD; A-->B" --output diagram.png
    python validate_mermaid.py --file diagram.mmd --output diagram.png --json
    python validate_mermaid.py --code "..." --context api_design --num 1 --title auth_flow

Requirements:
    mermaid-cli: npm install -g @mermaid-js/mermaid-cli
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


_USE_SHELL = sys.platform == "win32"


def check_mmdc() -> bool:
    try:
        subprocess.run(["mmdc", "--version"], capture_output=True, timeout=10, shell=_USE_SHELL)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


def validate_diagram(mmd_path: Path, output_path: Path, fmt: str = "png") -> dict:
    """Validate and render a .mmd file. Returns structured result."""
    try:
        result = subprocess.run(
            ["mmdc", "-i", str(mmd_path), "-o", str(output_path), "-b", "transparent"],
            capture_output=True, text=True, timeout=30, shell=_USE_SHELL,
        )
        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr.strip() or "Unknown render error",
                "input": str(mmd_path),
            }
        if not output_path.exists() or output_path.stat().st_size == 0:
            return {"success": False, "error": "Render produced no output", "input": str(mmd_path)}
        return {
            "success": True,
            "input": str(mmd_path),
            "output": str(output_path),
            "size_bytes": output_path.stat().st_size,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Render timed out (30s)", "input": str(mmd_path)}
    except Exception as e:
        return {"success": False, "error": str(e), "input": str(mmd_path)}


def resilient_render(
    mmd_code: str,
    output_path: Path,
    context: str = "diagram",
    diagram_num: int = 1,
    title: str = "untitled",
    fmt: str = "png",
    diagrams_dir: Path | None = None,
) -> dict:
    """Full resilient workflow: save .mmd, render, return structured result."""
    if diagrams_dir is None:
        diagrams_dir = Path("./diagrams")
    diagrams_dir.mkdir(parents=True, exist_ok=True)

    # Determine diagram type from first line
    first_line = mmd_code.strip().split("\n")[0].lower()
    dtype = "flowchart"
    for t in ["sequence", "class", "state", "er", "gantt", "pie", "mindmap", "c4context"]:
        if t in first_line:
            dtype = t
            break

    mmd_name = f"{context}_{diagram_num:02d}_{dtype}_{title}.mmd"
    mmd_path = diagrams_dir / mmd_name
    mmd_path.write_text(mmd_code, encoding="utf-8")

    if output_path is None:
        output_path = diagrams_dir / mmd_name.replace(".mmd", f".{fmt}")

    result = validate_diagram(mmd_path, output_path, fmt)
    result["mmd_file"] = str(mmd_path)
    result["naming"] = {"context": context, "num": diagram_num, "type": dtype, "title": title}
    return result


def main():
    parser = argparse.ArgumentParser(description="Resilient Mermaid validation")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--code", help="Mermaid code as string")
    group.add_argument("--file", type=Path, help="Path to .mmd file")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output image path")
    parser.add_argument("--format", default="png", choices=["png", "svg", "pdf"], help="Output format")
    parser.add_argument("--context", default="diagram", help="Context for file naming")
    parser.add_argument("--num", type=int, default=1, help="Diagram number")
    parser.add_argument("--title", default="untitled", help="Diagram title for naming")
    parser.add_argument("--diagrams-dir", type=Path, default=None, help="Directory for diagram files")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if not check_mmdc():
        err = {"success": False, "error": "mmdc not found. Install: npm install -g @mermaid-js/mermaid-cli"}
        print(json.dumps(err) if args.json else f"ERROR: {err['error']}", file=sys.stderr)
        sys.exit(1)

    if args.code:
        result = resilient_render(
            args.code, args.output, args.context, args.num, args.title, args.format, args.diagrams_dir
        )
    else:
        if not args.file.exists():
            print(f"ERROR: {args.file} not found", file=sys.stderr)
            sys.exit(1)
        code = args.file.read_text(encoding="utf-8")
        output = args.output or args.file.with_suffix(f".{args.format}")
        result = validate_diagram(args.file, output, args.format)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            print(f"✅ {result.get('output', result.get('mmd_file'))}")
        else:
            print(f"❌ {result['error']}", file=sys.stderr)

    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
