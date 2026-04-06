# Awesome Repos 🚀

Curated list of awesome repositories, auto-updated 2x weekly from my starred repos + GitHub trending.

Categories are assigned automatically via Claude AI.

**Last updated:** (pending first run)

---

## Setup

### Prerequisites

- Python 3.11+
- GitHub Personal Access Token with `repo`, `workflow`, `read:org`, `read:packages` scopes
- Anthropic API Key (for Claude Haiku categorization)

### Local Usage

```bash
cd scripts
pip install -r requirements.txt

export GH_TOKEN="your-github-token"
export ANTHROPIC_API_KEY="your-anthropic-api-key"

python fetch_and_categorize.py
```

### GitHub Actions Setup (Auto-Updates)

The workflow runs automatically every **Tuesday & Friday at 09:00 CET**.

To enable it:

1. Go to **Settings → Secrets and variables → Actions**
2. Create a new repository secret:
   - **Name:** `ANTHROPIC_API_KEY`
   - **Value:** Your Anthropic API key from [console.anthropic.com](https://console.anthropic.com)
3. Save ✅

That's it! The workflow will run on schedule and auto-commit updates.

---

## Categories

- **AI Agents** — Multi-agent systems, AI orchestration frameworks
- **Memory Systems** — Knowledge management, vault automation, persistent context
- **Finance/Trading** — Quant research, market analysis, trading bots
- **Claude Ecosystem** — Tools, skills, and integrations for Claude AI
- **DevTools** — Developer utilities, CLI tools, automation
- **Web Frameworks** — Backend/frontend frameworks, libraries
- **Data Science** — ML, analytics, scientific computing
- **Infrastructure** — Deployment, monitoring, DevOps
- **Other** — Everything else

---

## Contributing

Found a repo that should be here? Open an issue or PR!

## License

MIT — feel free to use this as inspiration for your own awesome list.
