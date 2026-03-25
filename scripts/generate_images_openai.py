#!/usr/bin/env python3
"""Generate images for all prompts using OpenAI Images API.

This script:
- Reads prompts/prompts.json (created by scripts/extract_prompts.py)
- Calls the OpenAI Images API for each prompt
- Saves resulting PNG files into renders/

Prerequisites:
- Python 3.10+
- An API key in env var OPENAI_API_KEY

Usage:
  python3 scripts/extract_prompts.py
  OPENAI_API_KEY="..." python3 scripts/generate_images_openai.py

Optional env vars:
- OPENAI_IMAGE_MODEL (default: gpt-image-1)
- OPENAI_IMAGE_SIZE (default: 1536x1024)
- OPENAI_IMAGE_QUALITY (default: high)
- OPENAI_IMAGE_STYLE (default: natural)
- OPENAI_IMAGE_N (default: 1)
"""

from __future__ import annotations

import base64
import json
import os
import re
import time
from pathlib import Path
from typing import Any

import urllib.request


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "prompts" / "prompts.json"
OUT_DIR = ROOT / "renders"

API_URL = "https://api.openai.com/v1/images/generations"


def sanitize_filename(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\-_.]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def request_image(
    api_key: str,
    prompt: str,
    model: str,
    size: str,
    quality: str,
    style: str,
    n: int,
) -> list[bytes]:
    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "style": style,
        "n": n,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=180) as resp:
        body = resp.read().decode("utf-8")

    parsed = json.loads(body)
    if "data" not in parsed:
        raise RuntimeError(f"Unexpected response: {parsed}")

    images: list[bytes] = []
    for item in parsed["data"]:
        # API typically returns b64_json.
        b64 = item.get("b64_json")
        if not b64:
            raise RuntimeError(f"No b64_json in response item: {item.keys()}")
        images.append(base64.b64decode(b64))

    return images


def main() -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Missing OPENAI_API_KEY env var.")

    model = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")
    size = os.environ.get("OPENAI_IMAGE_SIZE", "1536x1024")
    quality = os.environ.get("OPENAI_IMAGE_QUALITY", "high")
    style = os.environ.get("OPENAI_IMAGE_STYLE", "natural")
    n = int(os.environ.get("OPENAI_IMAGE_N", "1"))

    if not MANIFEST.exists():
        raise SystemExit("prompts/prompts.json not found. Run scripts/extract_prompts.py first.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    items = manifest.get("items", [])
    if not items:
        raise SystemExit("No items in prompts/prompts.json")

    total = len(items)
    for idx, it in enumerate(items, start=1):
        key = str(it.get("key", f"{idx:02d}"))
        title = str(it.get("title", "prompt"))
        prompt = str(it.get("prompt", ""))
        if not prompt.strip():
            continue

        base_name = sanitize_filename(f"{key}-{title}")

        # Skip if already generated
        existing = sorted(OUT_DIR.glob(f"{base_name}-*.png"))
        if existing:
            print(f"[{idx}/{total}] Skip {key} (already have {len(existing)} file(s))")
            continue

        print(f"[{idx}/{total}] Generating {key} — {title}")
        try:
            pngs = request_image(
                api_key=api_key,
                prompt=prompt,
                model=model,
                size=size,
                quality=quality,
                style=style,
                n=n,
            )
        except Exception as e:
            print(f"ERROR generating {key}: {e}")
            # Backoff to reduce rate-limit issues
            time.sleep(5)
            continue

        for j, png in enumerate(pngs, start=1):
            out_path = OUT_DIR / f"{base_name}-{j}.png"
            out_path.write_bytes(png)

        # Gentle pacing
        time.sleep(1)

    print(f"Done. Images in: {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
