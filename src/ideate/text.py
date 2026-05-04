from __future__ import annotations

import hashlib
import re
from textwrap import dedent


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:72].strip("-") or "idea"


def ranchi_codename(value: str, max_len: int = 12) -> str:
    """Return a short, deterministic, one-word codename inspired by Ranchi landmarks."""
    roots = [
        "harmu",
        "kanke",
        "dhurwa",
        "ratu",
        "birsa",
        "tagore",
        "jonha",
        "patra",
        "subar",
        "morha",
    ]
    base = slugify(value) or "idea"
    seed = int(hashlib.sha1(base.encode("utf-8")).hexdigest(), 16)
    root = roots[seed % len(roots)]
    alpha = "abcdefghijklmnopqrstuvwxyz"
    suffix = alpha[(seed // len(roots)) % 26] + alpha[(seed // (len(roots) * 26)) % 26]
    return f"{root}{suffix}"[:max_len]


def md(title: str, body: str) -> str:
    return f"# {title}\n\n{clean_md(body)}\n"


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def clean_md(body: str) -> str:
    text = dedent(body).strip()
    lines = text.splitlines()
    cleaned: list[str] = []
    for line in lines:
        if line.startswith("        ") and not line.startswith("        ```"):
            cleaned.append(line[8:])
        else:
            cleaned.append(line.rstrip())
    return "\n".join(cleaned).strip()
