from __future__ import annotations

import re
from textwrap import dedent


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:72].strip("-") or "idea"


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
