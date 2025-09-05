import requests
import os
from datetime import datetime, timezone

# ----- CONFIG -----
GITHUB_ORG = "y-sunflower"
REPOS = [
    "pypalettes",
    "pyfonts",
    "morethemes",
    "drawarrow",
    "dayplot",
    "plotjs",
    "bumplot",
]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
README_FILE = "README.md"
# ------------------


def human_timedelta(dt):
    now = datetime.now(timezone.utc)
    diff = now - dt

    seconds = int(diff.total_seconds())
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    weeks = days // 7
    months = days // 30

    if seconds < 60:
        return f"{seconds}s ago"
    elif minutes < 60:
        return f"{minutes}m ago"
    elif hours < 24:
        return f"{hours}h ago"
    elif days < 7:
        return f"{days}d ago"
    elif weeks < 5:
        return f"{weeks}w ago"
    else:
        return f"{months}mo ago"


def get_repo_data(repo):
    repo_url = f"https://api.github.com/repos/{GITHUB_ORG}/{repo}"

    r = requests.get(repo_url, headers=HEADERS).json()
    last_commit_date = r["pushed_at"]

    issues_r = requests.get(f"{repo_url}/issues?state=open", headers=HEADERS).json()
    open_issues = len([i for i in issues_r if "pull_request" not in i])

    prs_r = requests.get(
        f"{repo_url}/pulls?state=open&per_page=1", headers=HEADERS
    ).json()
    open_prs = len(prs_r)

    last_commit = datetime.strptime(last_commit_date, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc
    )
    last_commit_str = human_timedelta(last_commit)

    print(repo)
    print(f"issues: {open_issues}")
    print(f"prs: {open_prs}")
    print(f"last_commit: {last_commit_str}")
    print("\n")
    return {
        "name": repo,
        "issues": open_issues,
        "prs": open_prs,
        "last_commit": last_commit_str,
    }


def generate_readme(data):
    lines = [
        "# Y-Sunflower Projects Overview\n",
        "| Project | Open Issues | Open PRs | Last Commit |",
        "|---------|------------|----------|-------------|",
    ]

    for repo in data:
        lines.append(
            f"| [{repo['name']}](https://github.com/{GITHUB_ORG}/{repo['name']}) "
            f"| {repo['issues']} | {repo['prs']} | {repo['last_commit']} |"
        )

    return "\n".join(lines)


def main():
    data = [get_repo_data(repo) for repo in REPOS]
    readme_content = generate_readme(data)
    with open(README_FILE, "w") as f:
        f.write(readme_content)


if __name__ == "__main__":
    main()
