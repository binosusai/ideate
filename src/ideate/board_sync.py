from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable
from urllib import error, parse, request

from .models import Idea


@dataclass(frozen=True)
class AgentTaskUpdate:
    agent_name: str
    status: str
    output: str = ""


def _enabled() -> bool:
    return os.environ.get("IDEATE_GITHUB_TASK_BOARD", "1") == "1"


def _token() -> str | None:
    return os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")


def _repo() -> str | None:
    value = os.environ.get("IDEATE_TASKS_REPO") or os.environ.get("GITHUB_REPOSITORY")
    if not value or "/" not in value:
        return None
    return value


def _slug(value: str, max_len: int = 24) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return (text[:max_len].strip("-") or "task")


def _api(method: str, path: str, token: str, payload: dict | None = None) -> dict:
    url = f"https://api.github.com{path}"
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "ideate-agent-board-sync",
            "Content-Type": "application/json",
        },
    )
    with request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}


def _ensure_label(owner: str, repo: str, token: str, name: str, color: str, description: str) -> None:
    try:
        _api(
            "POST",
            f"/repos/{owner}/{repo}/labels",
            token,
            {
                "name": name,
                "color": color,
                "description": description[:100],
            },
        )
    except error.HTTPError as exc:
        # 422 = already exists
        if exc.code != 422:
            raise


def _find_issue_number(owner: str, repo: str, token: str, task_key: str) -> int | None:
    query = f"repo:{owner}/{repo} in:body \"{task_key}\" is:issue"
    path = "/search/issues?q=" + parse.quote(query)
    data = _api("GET", path, token)
    items = data.get("items", [])
    if not items:
        return None
    return int(items[0]["number"])


def _upsert_issue(
    owner: str,
    repo: str,
    token: str,
    task_key: str,
    title: str,
    body: str,
    labels: list[str],
    state: str,
) -> None:
    number = _find_issue_number(owner, repo, token, task_key)
    payload = {
        "title": title,
        "body": body,
        "labels": labels,
        "state": state,
    }
    if number is None:
        _api("POST", f"/repos/{owner}/{repo}/issues", token, payload)
    else:
        _api("PATCH", f"/repos/{owner}/{repo}/issues/{number}", token, payload)


def sync_agent_tasks(idea: Idea, stage: str, tasks: Iterable[AgentTaskUpdate]) -> None:
    if not _enabled():
        return
    repo = _repo()
    token = _token()
    if not repo or not token:
        return

    owner, repo_name = repo.split("/", 1)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    base_labels = [
        "ideate-task",
        f"idea:{idea.id}",
        f"stage:{_slug(stage, max_len=20)}",
    ]
    static_labels = {
        "ideate-task": ("1f6feb", "Ideate agent task item"),
        f"idea:{idea.id}": ("bfd4f2", "Idea identifier"),
        f"stage:{_slug(stage, max_len=20)}": ("d4c5f9", "Pipeline stage"),
        "task:in-progress": ("f9d458", "Agent task currently running"),
        "task:done": ("2da44e", "Agent task completed"),
    }
    for name, (color, desc) in static_labels.items():
        _ensure_label(owner, repo_name, token, name, color, desc)

    for task in tasks:
        agent_label = f"agent:{_slug(task.agent_name, max_len=20)}"
        _ensure_label(owner, repo_name, token, agent_label, "fbca04", "Agent role")
        status_label = "task:done" if task.status == "done" else "task:in-progress"
        task_key = f"ideate-task:{idea.id}:{_slug(stage, 20)}:{_slug(task.agent_name, 20)}"

        output_block = task.output.strip()
        if output_block:
            output_block = output_block[:3500]
            details = f"\n\n## Agent Output\n\n{output_block}"
        else:
            details = "\n\n## Agent Output\n\nPending..."

        body = (
            f"<!-- {task_key} -->\n"
            f"# Ideate Agent Task\n\n"
            f"- Idea: #{idea.id} {idea.title}\n"
            f"- Stage: {stage}\n"
            f"- Agent: {task.agent_name}\n"
            f"- Status: {task.status}\n"
            f"- Updated: {now}"
            + details
        )
        title = f"Idea {idea.id} | {stage.title()} | {task.agent_name}"
        labels = [*base_labels, agent_label, status_label]
        state = "closed" if task.status == "done" else "open"
        _upsert_issue(owner, repo_name, token, task_key, title, body, labels, state)
