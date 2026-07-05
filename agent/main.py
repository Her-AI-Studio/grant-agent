"""Grant Agent — main orchestrator that runs the weekly grant search pipeline."""

import asyncio
import os
from datetime import datetime

from agent.sources import SOURCES
from agent.search import search_source
from agent.storage import (
    is_grant_seen,
    mark_grant_seen,
)
from agent.emailer import render_email_html, send_email


# ── Configuration ──────────────────────────────────────────────────────────────

ORGANIZATION_NAME = os.environ.get(
    "ORG_NAME", "Her AI Studio"
)
ORGANIZATION_MISSION = os.environ.get(
    "ORG_MISSION",
    "Teach middle school girls AI, robotics, physical computing, "
    "responsible AI, and creative technology.",
)


# ── Pipeline ───────────────────────────────────────────────────────────────────


async def run_pipeline() -> None:
    """Execute the full grant search → email pipeline."""
    print("=" * 60)
    print(f"Grant Agent — {datetime.utcnow().isoformat()}")
    print(f"Organization: {ORGANIZATION_NAME}")
    print("=" * 60)

    # 1. Search all sources
    print("\n[1/3] Searching grant sources...")
    all_grants: list[dict] = []
    for source in SOURCES:
        grants = await search_source(source)
        all_grants.extend(grants)

    print(f"\n  Found {len(all_grants)} total grant entries across {len(SOURCES)} sources.")

    # 2. Filter out already-seen grants
    print("\n[2/3] Filtering already-seen grants...")
    new_grants = []
    for grant in all_grants:
        grant_id = grant.get("url", grant.get("title", ""))
        if not is_grant_seen(grant_id):
            new_grants.append(grant)
            mark_grant_seen(grant_id)

    print(f"  {len(new_grants)} new grants to report.")

    if not new_grants:
        print("\n[3/3] No new grants to report. Skipping email.")
        print("\n[Done]")
        return

    # 3. Generate and send email with all new grants
    print("\n[3/3] Generating and sending email report...")

    # Wrap each grant in a simple dict for template compatibility
    scored_grants = [(grant, {}) for grant in new_grants]

    html = render_email_html(
        organization_name=ORGANIZATION_NAME,
        scored_grants=scored_grants,
        total_sources=len(SOURCES),
        total_grants_found=len(all_grants),
    )

    today = datetime.utcnow().strftime("%B %d, %Y")
    subject = f"🧭 Weekly Grant Report — {ORGANIZATION_NAME} — {today}"

    send_email(subject=subject, html_body=html)

    print("\n" + "=" * 60)
    print("[Done] Weekly grant pipeline complete.")
    print("=" * 60)


def main() -> None:
    """Entry point for the grant agent."""
    asyncio.run(run_pipeline())


if __name__ == "__main__":
    main()