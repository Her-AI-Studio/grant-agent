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
        url="https://www.nsf.gov/rss/rss_grants_feed.xml",
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
        name="GitHub Social Impact",
        url="https://github.blog/category/social-impact/feed/",
        type="rss",
        description="GitHub grants, open-source funding, and social impact programs",
    ),
    GrantSource(
        name="Microsoft Philanthropies",
        url="https://www.microsoft.com/en-us/philanthropies/feed/",
        type="rss",
        description="Microsoft grants for nonprofits and education",
    ),
    GrantSource(
        name="NVIDIA",
        url="https://www.nvidia.com/en-us/about-nvidia/corporate-giving/",
        type="page",
        description="NVIDIA foundation grants and donation programs",
    ),
    GrantSource(
        name="Motorola Foundation",
        url="https://www.motorolasolutions.com/en_us/about/company-overview/corporate-responsibility/motorola-solutions-foundation.html",
        type="page",
        description="Motorola Solutions Foundation grant programs",
    ),
    GrantSource(
        name="Infosys Foundation USA",
        url="https://www.infosys.org/infosys-foundation-usa/",
        type="page",
        description="Infosys Foundation USA grants for CS education",
    ),
    GrantSource(
        name="AWS Imagine Grant",
        url="https://aws.amazon.com/grants/",
        type="page",
        description="AWS Imagine Grant for nonprofits using cloud technology",
    ),
]