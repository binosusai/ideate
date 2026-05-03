from __future__ import annotations

from dataclasses import dataclass


CATEGORIES = {"money", "personal"}
STATUSES = {
    "captured",
    "researched",
    "debated",
    "planned",
    "approved",
    "poc",
    "handoff",
    "in_progress",
    "completed",
    "paused",
    "killed",
}


@dataclass(frozen=True)
class Idea:
    id: int
    title: str
    slug: str
    category: str
    why: str
    status: str
    score: float
    created_at: str
    updated_at: str
