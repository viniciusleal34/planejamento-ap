#!/usr/bin/env python3
"""Extract prompts from docs/14-prompts-para-renders.md into prompts/.

Outputs:
- prompts/prompts.json (metadata + prompt text)
- prompts/*.txt (one file per prompt)

Usage:
  python3 scripts/extract_prompts.py
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = ROOT / "docs" / "14-prompts-para-renders.md"
OUT_DIR = ROOT / "prompts"


@dataclass(frozen=True)
class PromptItem:
    key: str
    title: str
    filename: str
    prompt: str


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[\u2014\u2013]", "-", text)
    text = re.sub(r"[^a-z0-9\s\-+()Ø².,]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_prompt_blocks(md: str) -> list[PromptItem]:
    # We consider prompts that follow headings like:
    # ### 01 — Title
    # then a fenced block ``` ... ```
    heading_re = re.compile(r"^###\s+([0-9]{2}[A-Z]?)\s+—\s+(.+?)\s*$", re.MULTILINE)

    items: list[PromptItem] = []
    for match in heading_re.finditer(md):
        key = match.group(1)
        title = match.group(2).strip()
        start = match.end()

        fence_start = md.find("```", start)
        if fence_start == -1:
            continue
        fence_end = md.find("```", fence_start + 3)
        if fence_end == -1:
            continue

        block = md[fence_start + 3 : fence_end]
        prompt = block.strip("\n")

        # Only keep blocks that look like prompts (contain PROJECT BASE or Create/Generate)
        if not prompt:
            continue

        filename = f"{key}-{slugify(title)[:60]}.txt"
        items.append(
            PromptItem(
                key=key,
                title=title,
                filename=filename,
                prompt=prompt,
            )
        )

    # Ensure deterministic ordering by key (handles 04B etc)
    def sort_key(item: PromptItem):
        m = re.match(r"^(\d+)([A-Z]?)$", item.key)
        if not m:
            return (999, item.key)
        num = int(m.group(1))
        suffix = m.group(2) or ""
        return (num, suffix)

    return sorted(items, key=sort_key)


def main() -> int:
    if not SOURCE_MD.exists():
        raise SystemExit(f"Source file not found: {SOURCE_MD}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    md = read_text(SOURCE_MD)
    items = find_prompt_blocks(md)

    if not items:
        raise SystemExit("No prompts found. Check the markdown headings and fenced blocks.")

    manifest = {
        "source": os.fspath(SOURCE_MD.relative_to(ROOT)),
        "count": len(items),
        "items": [
            {
                "key": it.key,
                "title": it.title,
                "file": os.fspath((OUT_DIR / it.filename).relative_to(ROOT)),
                "prompt": it.prompt,
            }
            for it in items
        ],
    }

    (OUT_DIR / "prompts.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    for it in items:
        (OUT_DIR / it.filename).write_text(it.prompt.strip() + "\n", encoding="utf-8")

    print(f"Extracted {len(items)} prompts to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
