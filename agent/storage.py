"""JSON-based storage for tracking seen grants to avoid duplicates."""

import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
GRANTS_FILE = os.path.join(DATA_DIR, "grants.json")


def _ensure_data_dir() -> None:
    """Create the data directory if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_seen_grants() -> dict:
    """Load the grants database. Returns dict with 'seen' key."""
    _ensure_data_dir()
    if not os.path.exists(GRANTS_FILE):
        return {"seen": []}
    with open(GRANTS_FILE) as f:
        return json.load(f)


def save_seen_grants(data: dict) -> None:
    """Persist the grants database to disk."""
    _ensure_data_dir()
    with open(GRANTS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def is_grant_seen(grant_id: str) -> bool:
    """Check if a grant has already been processed (by URL or unique ID)."""
    data = load_seen_grants()
    return grant_id in data.get("seen", [])


def mark_grant_seen(grant_id: str) -> None:
    """Add a grant to the seen list."""
    data = load_seen_grants()
    if "seen" not in data:
        data["seen"] = []
    if grant_id not in data["seen"]:
        data["seen"].append(grant_id)
    save_seen_grants(data)