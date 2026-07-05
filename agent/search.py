"""Grant search — fetches RSS feeds and scrapes web pages for grant opportunities."""

import re
from datetime import datetime
from typing import Optional

import feedparser
import httpx
from bs4 import BeautifulSoup

from agent.sources import GrantSource


async def fetch_rss(source: GrantSource) -> list[dict]:
    """Fetch and parse an RSS feed, returning a list of grant entries."""
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(source.url)
            response.raise_for_status()
    except Exception as e:
        print(f"  [WARN] Failed to fetch RSS {source.name}: {e}")
        return []

    feed = feedparser.parse(response.text)
    entries = []
    for entry in feed.entries[:20]:  # limit to 20 per source
        grant = {
            "title": entry.get("title", "Untitled"),
            "url": entry.get("link", ""),
            "description": _clean_html(entry.get("summary", entry.get("description", ""))),
            "source": source.name,
            "source_url": source.url,
            "deadline": _extract_deadline(entry),
            "amount": _extract_amount(entry),
            "found_at": datetime.utcnow().isoformat(),
        }
        entries.append(grant)
    return entries


async def fetch_page(source: GrantSource) -> list[dict]:
    """Fetch and scrape a web page for grant listings."""
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(source.url)
            response.raise_for_status()
    except Exception as e:
        print(f"  [WARN] Failed to fetch page {source.name}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)

    # Return the page content as a single grant entry for the LLM to analyze
    grant = {
        "title": f"{source.name} — Grant Programs",
        "url": source.url,
        "description": text[:3000],  # truncate to avoid token limits
        "source": source.name,
        "source_url": source.url,
        "deadline": "Not specified",
        "amount": "Not specified",
        "found_at": datetime.utcnow().isoformat(),
    }
    return [grant]


async def search_source(source: GrantSource) -> list[dict]:
    """Dispatch to the correct fetcher based on source type."""
    print(f"  Fetching {source.name} ({source.type})...")
    if source.type == "rss":
        return await fetch_rss(source)
    elif source.type == "page":
        return await fetch_page(source)
    else:
        print(f"  [WARN] Unknown source type: {source.type}")
        return []


def _clean_html(html: str) -> str:
    """Strip HTML tags and normalize whitespace."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def _extract_deadline(entry) -> str:
    """Try to extract a deadline from RSS entry fields."""
    for field in ["deadline", "close_date", "end_date"]:
        val = getattr(entry, field, None)
        if val:
            return str(val)
    # Try common RSS date fields
    for field in ["published", "updated", "dc_date"]:
        val = getattr(entry, field, None)
        if val:
            return str(val)
    return "Not specified"


def _extract_amount(entry) -> str:
    """Try to extract a dollar amount from RSS entry fields."""
    for field in ["award_amount", "amount", "funding"]:
        val = getattr(entry, field, None)
        if val:
            return str(val)
    # Try to find dollar amounts in the description
    desc = entry.get("summary", "") or entry.get("description", "")
    amounts = re.findall(r"\$[\d,]+(?:,\d{3})*(?:\.\d{2})?", desc)
    if amounts:
        return amounts[0]
    return "Not specified"