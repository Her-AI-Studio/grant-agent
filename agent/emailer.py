"""Email generation — creates and sends the weekly HTML grant report via Gmail SMTP."""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def _get_smtp_config() -> dict:
    """Read SMTP configuration from environment variables."""
    return {
        "smtp_host": os.environ.get("SMTP_HOST", "smtp.gmail.com"),
        "smtp_port": int(os.environ.get("SMTP_PORT", "587")),
        "smtp_user": os.environ.get("SMTP_USER", ""),
        "smtp_password": os.environ.get("SMTP_PASSWORD", ""),
        "from_email": os.environ.get("FROM_EMAIL", os.environ.get("SMTP_USER", "")),
        "to_email": os.environ.get("TO_EMAIL", ""),
    }


def render_email_html(
    organization_name: str,
    scored_grants: list[tuple[dict, dict]],
    total_sources: int,
    total_grants_found: int,
) -> str:
    """Render the weekly email HTML using the Jinja2 template."""
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("weekly_email.html")

    return template.render(
        organization_name=organization_name,
        scored_grants=scored_grants,
        total_sources=total_sources,
        total_grants_found=total_grants_found,
        total_scored=len(scored_grants),
    )


def send_email(
    subject: str,
    html_body: str,
    config: Optional[dict] = None,
) -> bool:
    """Send an HTML email via SMTP.

    Returns True on success, False on failure.
    """
    if config is None:
        config = _get_smtp_config()

    if not config["smtp_user"] or not config["smtp_password"]:
        print("[WARN] SMTP credentials not configured. Skipping email send.")
        print(f"[INFO] Email would have been sent to: {config['to_email']}")
        print(f"[INFO] Subject: {subject}")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = config["from_email"]
    msg["To"] = config["to_email"]

    part = MIMEText(html_body, "html", "utf-8")
    msg.attach(part)

    try:
        with smtplib.SMTP(config["smtp_host"], config["smtp_port"]) as server:
            server.starttls()
            server.login(config["smtp_user"], config["smtp_password"])
            server.sendmail(config["from_email"], config["to_email"], msg.as_string())
        print(f"[OK] Email sent to {config['to_email']}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        return False