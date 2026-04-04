#!/usr/bin/env python3
"""Inspect a workspace and summarize Power BI theme/template assets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize Power BI theme JSON and PBIT assets in a workspace."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Workspace directory to scan. Defaults to the current directory.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    return parser.parse_args()


def load_theme_summary(path: Path) -> dict:
    data = json.loads(path.read_text())
    styles = data.get("visualStyles", {}).get("*", {}).get("*", {})
    title = (styles.get("title") or [{}])[0]
    background = (styles.get("background") or [{}])[0]
    border = (styles.get("border") or [{}])[0]
    legend = (styles.get("legend") or [{}])[0]
    return {
        "path": str(path),
        "name": data.get("name"),
        "data_colors": data.get("dataColors", []),
        "background": background.get("color", {}).get("solid", {}).get("color"),
        "title_font_family": title.get("fontFamily"),
        "title_font_size": title.get("fontSize"),
        "legend_position": legend.get("position"),
        "border_radius": border.get("radius"),
    }


def scan(root: Path) -> dict:
    themes = []
    templates = []

    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        suffix = path.suffix.lower()
        if suffix == ".json":
            try:
                summary = load_theme_summary(path)
            except Exception:
                continue
            if summary["data_colors"]:
                themes.append(summary)
        elif suffix == ".pbit":
            templates.append({"path": str(path), "name": path.name})

    return {"root": str(root), "themes": themes, "templates": templates}


def emit_markdown(summary: dict) -> str:
    lines = [f"# Power BI Assets in `{summary['root']}`", ""]

    if summary["themes"]:
        lines.extend(["## Theme JSON", ""])
        for theme in summary["themes"]:
            colors = ", ".join(theme["data_colors"][:5])
            lines.append(f"- `{theme['path']}`")
            lines.append(
                f"  name={theme['name']}; title={theme['title_font_family']} {theme['title_font_size']}; "
                f"bg={theme['background']}; legend={theme['legend_position']}; border_radius={theme['border_radius']}; "
                f"data_colors={colors}"
            )
        lines.append("")
    else:
        lines.extend(["## Theme JSON", "", "- none found", ""])

    if summary["templates"]:
        lines.extend(["## PBIT Templates", ""])
        for template in summary["templates"]:
            lines.append(f"- `{template['path']}`")
        lines.append("")
    else:
        lines.extend(["## PBIT Templates", "", "- none found", ""])

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    summary = scan(root)
    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(emit_markdown(summary), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
