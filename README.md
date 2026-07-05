# Grant Agent 🧭

An automated grant scouting agent that searches grant sources and emails you a weekly report of new opportunities.

Built for **Her AI Studio** — teaching middle school girls AI, robotics, physical computing, responsible AI, and creative technology.

## How It Works

Every Monday at 7:00 AM Eastern, the agent runs via GitHub Actions:

1. **Search** — Fetches grant listings from 10+ sources (RSS feeds + web scraping)
2. **Filter** — Skips grants already seen (tracked in `data/grants.json`)
3. **Report** — Emails an HTML newsletter with all new opportunities

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.12 |
| RSS Parsing | feedparser |
| Web Scraping | httpx + beautifulsoup4 |
| Email Templates | Jinja2 |
| Email Delivery | Gmail SMTP |
| Scheduling | GitHub Actions (cron) |
| Storage | JSON file (`data/grants.json`) |

## Repository Structure

```
grant-agent/
├── .github/workflows/weekly.yml   # GitHub Actions schedule
├── agent/
│   ├── main.py                     # Pipeline orchestrator
│   ├── search.py                   # RSS & web page fetchers
│   ├── sources.py                  # Grant source definitions
│   ├── emailer.py                  # HTML email generation & sending
│   └── storage.py                  # JSON-based seen-grant tracker
├── templates/
│   └── weekly_email.html           # Jinja2 email template
├── data/
│   └── grants.json                 # Seen grants database
├── requirements.txt
└── README.md
```

## Grant Sources (Week 1)

| Source | Type |
|--------|------|
| Grants.gov | RSS |
| National Science Foundation | RSS |
| Department of Education | RSS |
| Google.org | RSS |
| GitHub Social Impact | RSS |
| Microsoft Philanthropies | RSS |
| NVIDIA | Web page |
| Motorola Foundation | Web page |
| Infosys Foundation USA | Web page |
| AWS Imagine Grant | Web page |

## Setup

### 1. Repository Secrets

Add these secrets to your GitHub repository (**Settings → Secrets and variables → Actions**):

| Secret | Description |
|--------|-------------|
| `SMTP_USER` | Gmail address for sending emails |
| `SMTP_PASSWORD` | Gmail app password (not your regular password) |
| `FROM_EMAIL` | Sender email address |
| `TO_EMAIL` | Recipient email address |

Optional secrets:
- `ORG_NAME` — Your organization name (default: "Her AI Studio")
- `ORG_MISSION` — Your organization's mission statement
- `SMTP_HOST` — SMTP server (default: `smtp.gmail.com`)
- `SMTP_PORT` — SMTP port (default: `587`)

### 2. Gmail App Password (Step-by-Step)

Gmail requires an **App Password** instead of your regular password when sending via SMTP. Here's how to get one:

1. **Enable 2-Step Verification** on your Google account:
   - Go to https://myaccount.google.com/security
   - Under "How you sign in to Google," click **2-Step Verification**
   - Follow the prompts to turn it on (you'll need a phone number for backup)

2. **Generate an App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - You may need to sign in again
   - Under "Select app," choose **Mail**
   - Under "Select device," choose **Other (Custom name)**
   - Type `grant-agent` and click **Generate**
   - Google will show you a 16-character password (e.g., `xxxx xxxx xxxx xxxx`)
   - **Copy this password immediately** — you won't be able to see it again

3. **Use the App Password**:
   - `SMTP_USER` = your full Gmail address (e.g., `you@gmail.com`)
   - `SMTP_PASSWORD` = the 16-character app password (with or without spaces — both work)
   - `FROM_EMAIL` = your Gmail address
   - `TO_EMAIL` = where you want the reports sent (can be the same address)

> ⚠️ If you don't see the App Passwords option, make sure 2-Step Verification is fully enabled first. It can take a few minutes to propagate.

### 3. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ORG_NAME="Her AI Studio"
export ORG_MISSION="Teach middle school girls AI, robotics, physical computing, responsible AI, and creative technology."
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export TO_EMAIL="you@example.com"

# Run the agent
python -m agent.main
```

## Email Report

The weekly email includes:
- **Stats bar** — sources checked, grants found, new this week
- **New Grant Opportunities** — each grant card shows: title, source, description, deadline, amount, and a "View Grant" link

## Customization

### Adding Sources

Edit `agent/sources.py` and add a new `GrantSource`:

```python
GrantSource(
    name="Your Source",
    url="https://example.com/feed.xml",
    type="rss",  # or "page" for web scraping
    description="Description of the source",
)
```

### Changing the Schedule

Edit the cron expression in `.github/workflows/weekly.yml`:

```yaml
- cron: "0 11 * * 1"  # Current: Monday 11:00 UTC
```

## Future Enhancements

- [ ] AI-powered grant scoring (OpenAI integration)
- [ ] PDF parsing for grant application documents
- [ ] Document generation (cover letters, budgets)
- [ ] More grant sources
- [ ] Slack/Discord notifications
- [ ] Dashboard with grant pipeline tracking
- [ ] Multi-organization support

## License

MIT