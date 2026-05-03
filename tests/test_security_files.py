from __future__ import annotations

from pathlib import Path


def test_secret_files_are_ignored() -> None:
    root = Path(__file__).resolve().parents[2]
    gitignore = (root / ".gitignore").read_text(encoding="utf-8")
    codexignore = (root / ".codexignore").read_text(encoding="utf-8")

    assert ".env" in gitignore
    assert "**/.env" in gitignore
    assert ".env" in codexignore
    assert "**/.env" in codexignore
