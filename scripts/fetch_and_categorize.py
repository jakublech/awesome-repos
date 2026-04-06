#!/usr/bin/env python3
"""
Fetch starred repos + GitHub trending, categorize via Claude Haiku API.
Updates README.md with curated list sorted by category.
"""

import os
import json
import subprocess
from datetime import datetime
from collections import defaultdict
import requests
from anthropic import Anthropic

GH_TOKEN = os.environ.get('GH_TOKEN')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

if not GH_TOKEN or not ANTHROPIC_API_KEY:
    raise ValueError("GH_TOKEN and ANTHROPIC_API_KEY environment variables required")

# Initialize Anthropic client
client = Anthropic(api_key=ANTHROPIC_API_KEY)

DEFAULT_CATEGORIES = [
    "AI Agents",
    "Memory Systems",
    "Finance/Trading",
    "Claude Ecosystem",
    "DevTools",
    "Web Frameworks",
    "Data Science",
    "Infrastructure",
    "Other"
]

def fetch_starred_repos():
    """Fetch all starred repos from authenticated user."""
    headers = {'Authorization': f'token {GH_TOKEN}'}
    repos = []
    page = 1
    
    while True:
        resp = requests.get(
            f'https://api.github.com/user/starred?per_page=100&page={page}',
            headers=headers
        )
        resp.raise_for_status()
        data = resp.json()
        
        if not data:
            break
        
        repos.extend(data)
        page += 1
    
    return repos

def fetch_trending_repos():
    """Fetch trending repos from GitHub trending page (scrape fallback)."""
    # For now, return empty — can be extended with BeautifulSoup scraping
    return []

def categorize_repo(repo_data):
    """Use Claude Haiku to categorize repo based on description + name."""
    name = repo_data.get('name', '')
    description = repo_data.get('description', '')
    url = repo_data.get('html_url', '')
    topics = repo_data.get('topics', [])
    language = repo_data.get('language', 'Unknown')
    stars = repo_data.get('stargazers_count', 0)
    
    prompt = f"""Categorize this GitHub repo into ONE of these categories:
{', '.join(DEFAULT_CATEGORIES)}

Repo:
- Name: {name}
- Description: {description}
- URL: {url}
- Topics: {', '.join(topics) if topics else 'None'}
- Language: {language}
- Stars: {stars}

Respond with ONLY the category name, nothing else."""
    
    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=50,
        messages=[{"role": "user", "content": prompt}]
    )
    
    category = message.content[0].text.strip()
    
    # Validate category
    if category not in DEFAULT_CATEGORIES:
        category = "Other"
    
    return category

def format_repo_entry(repo_data):
    """Format single repo as markdown entry."""
    name = repo_data.get('name', '')
    description = repo_data.get('description', '') or '(No description)'
    url = repo_data.get('html_url', '')
    stars = repo_data.get('stargazers_count', 0)
    language = repo_data.get('language', 'Unknown')
    
    return f"- **[{name}]({url})** — {description} `{language}` ⭐ {stars}"

def generate_readme(categorized_repos):
    """Generate README.md from categorized repos."""
    readme = """# Awesome Repos 🚀

Curated list of awesome repositories, auto-updated 2x weekly from my starred repos + GitHub trending.

Categories are assigned automatically via Claude AI.

**Last updated:** {}

---

""".format(datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'))
    
    for category in DEFAULT_CATEGORIES:
        repos = categorized_repos.get(category, [])
        if repos:
            readme += f"\n## {category}\n\n"
            for repo in sorted(repos, key=lambda r: r.get('stargazers_count', 0), reverse=True):
                readme += format_repo_entry(repo) + "\n"
    
    readme += """\n---

## Setup

To use this repo:

1. Clone it
2. No dependencies — this is a curated markdown list
3. Watch or star to get updates on every Tuesday & Friday at 09:00 CET

## Contributing

Found a repo that should be here? Open an issue or PR!

## License

MIT — feel free to use this as inspiration for your own awesome list.
"""
    
    return readme

def main():
    print("[*] Fetching starred repos...")
    starred = fetch_starred_repos()
    print(f"[+] Found {len(starred)} starred repos")
    
    print("[*] Fetching trending repos...")
    trending = fetch_trending_repos()
    print(f"[+] Found {len(trending)} trending repos")
    
    all_repos = starred + trending
    print(f"[*] Total repos to categorize: {len(all_repos)}")
    
    # Categorize repos
    categorized = defaultdict(list)
    for i, repo in enumerate(all_repos, 1):
        print(f"[{i}/{len(all_repos)}] Categorizing {repo.get('name')}...", end=' ', flush=True)
        try:
            category = categorize_repo(repo)
            categorized[category].append(repo)
            print(f"→ {category}")
        except Exception as e:
            print(f"ERROR: {e}")
            categorized["Other"].append(repo)
    
    # Generate README
    print("[*] Generating README.md...")
    readme = generate_readme(categorized)
    
    with open('README.md', 'w') as f:
        f.write(readme)
    
    print("[+] README.md updated successfully")
    print(f"[+] Total repos: {len(all_repos)}")
    for category, repos in sorted(categorized.items()):
        print(f"    {category}: {len(repos)}")

if __name__ == '__main__':
    main()
