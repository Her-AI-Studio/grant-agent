"""Grant source definitions — RSS feeds, grant URLs, and metadata for each source."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GrantSource:
    name: str
    url: str
    type: str  # "rss" | "page"
    description: str
    logo_url: Optional[str] = None


SOURCES: list[GrantSource] = [
    GrantSource(
        name="Grants.gov",
        url="https://www.grants.gov/rss/grants_feed.xml",
        type="rss",
        description="U.S. federal government grant opportunities",
    ),
    GrantSource(
        name="National Science Foundation",
        url="https://www.nsf.gov/rss/rss_www_funding_pgm_annc_inf.xml",
        type="rss",
        description="NSF funding opportunities across all sciences",
    ),
    GrantSource(
        name="Department of Education",
        url="https://www.ed.gov/feed/grant-opportunities",
        type="rss",
        description="Federal education grants and programs",
    ),
    GrantSource(
        name="Google.org",
        url="https://blog.google/outreach-initiatives/google-org/rss/",
        type="rss",
        description="Google philanthropic funding and AI for Social Good",
    ),
  
    GrantSource(
        name="Mozilla Open Source Support",
        url="https://www.mozillafoundation.org/en/what-we-do/grantmaking/",
        type="rss",
        description="Mozilla grants for open-source software projects",
    ),

    GrantSource(
        name="Motorola Foundation",
        url="https://www.motorolasolutions.com/en_us/about/company-overview/corporate-responsibility/motorola-solutions-foundation.html",
        type="page",
        description="Motorola Solutions Foundation grant programs",
    )
]