from __future__ import annotations

import shutil
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    git_dir = root / ".git"
    if not git_dir.exists():
        print("No .git directory found under ideate; initialize git before installing hooks.")
        return 1

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    source = root / "hooks" / "pre-commit"
    target = hooks_dir / "pre-commit"
    shutil.copyfile(source, target)
    target.chmod(0o755)
    print(f"Installed {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
