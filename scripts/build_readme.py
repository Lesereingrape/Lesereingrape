#!/usr/bin/env python3
"""Render the profile README from live GitHub data.

Stdlib only so it can run inside a bare ubuntu-latest workflow. Reads the
token from GITHUB_TOKEN / GH_TOKEN, falling back to `gh auth token` for
local runs.

    python scripts/build_readme.py [--write]   # --write updates README.md
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from collections import Counter, defaultdict

OWNER = (
    os.environ.get("PROFILE_OWNER")
    or os.environ.get("GITHUB_REPOSITORY_OWNER")
    or "Lesereingrape"
)
MIN_STARS = int(os.environ.get("MIN_STARS", "1000"))
API = "https://api.github.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
FLAGSHIPS = os.path.join(ROOT, "scripts", "flagships.json")
STAMP_RE = re.compile(r"record last changed \d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC")

_badge = "https://img.shields.io/badge/"


def _token() -> str:
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        return tok.strip()
    out = subprocess.run(
        ["gh", "auth", "token"], capture_output=True, text=True, encoding="utf-8"
    )
    if out.returncode == 0 and out.stdout.strip():
        return out.stdout.strip()
    raise SystemExit("no GitHub token: set GITHUB_TOKEN or install gh")


TOKEN = _token()


def get(url: str):
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-readme-builder",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        stamp = resp.headers.get("Date")
        if stamp and not STATE["server_date"]:
            # Trust GitHub's clock, not the runner's, for the build stamp.
            STATE["server_date"] = stamp
        return json.load(resp)


STATE = {"server_date": ""}


def search(query: str) -> list[dict]:
    items: list[dict] = []
    page = 1
    while page <= 10:
        batch = get(
            f"{API}/search/issues"
            f"?q={urllib.parse.quote(query)}&per_page=100&page={page}"
        )
        found = batch.get("items") or []
        items.extend(found)
        if not found or len(items) >= batch.get("total_count", 0):
            return items
        page += 1
    return items


def repo_full(item: dict) -> str:
    return item["repository_url"].split("/repos/", 1)[1]


def stars_for(full: str) -> int:
    return int(get(f"{API}/repos/{full}").get("stargazers_count") or 0)


def stars_text(n: int) -> str:
    if n >= 1000:
        return f"{n / 1000:.1f}K"
    return str(n)


def load_flagships() -> dict:
    with open(FLAGSHIPS, encoding="utf-8") as fh:
        return json.load(fh)


def flagship_names(spec: dict) -> list[str]:
    return [e["repo"] for t in spec["tracks"] for e in t["repos"]]


def fetch_own(names: list[str]) -> tuple[dict[str, dict], list[str]]:
    """Read every curated repository straight from the API.

    A hand-kept list rots the moment a repo is renamed, made private, or loses
    its description, so the build refuses to publish a link it cannot verify
    instead of putting a 404 on the profile page.
    """
    repos: dict[str, dict] = {}
    problems: list[str] = []
    for name in names:
        full = f"{OWNER}/{name}"
        try:
            data = get(f"{API}/repos/{full}")
        except Exception as exc:  # noqa: BLE001 - reported, never published
            problems.append(f"{full}: unreadable ({exc})")
            continue
        if data.get("private"):
            problems.append(f"{full}: private")
            continue
        if not (data.get("description") or "").strip():
            problems.append(f"{full}: no description")
            continue
        repos[name] = data
    return repos, problems


def badge(label: str, value: str, color: str, logo: str = "") -> str:
    q = f"?style=flat-square&labelColor=1b1f24&color={color}"
    if logo:
        q += f"&logo={logo}&logoColor=white"
    url = f"{_badge}{label.replace(' ', '__')}-{value.replace(' ', '__')}-{color}{q}"
    return f"![{label} {value}]({url})"


def month_of(iso: str) -> str:
    return dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%Y-%m")


def build_stamp() -> str:
    raw = STATE["server_date"]
    if not raw:
        return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    parsed = dt.datetime.strptime(raw, "%a, %d %b %Y %H:%M:%S %Z").replace(
        tzinfo=dt.timezone.utc
    )
    return parsed.strftime("%Y-%m-%d %H:%M UTC")


def render(
    merged: list[dict], open_prs: list[dict], stars: dict[str, int], own: dict
) -> str:
    by_repo: dict[str, list[dict]] = defaultdict(list)
    for pr in merged:
        by_repo[repo_full(pr)].append(pr)
    shown = {r: v for r, v in by_repo.items() if stars.get(r, 0) >= MIN_STARS}
    excluded = {r: v for r, v in by_repo.items() if r not in shown}
    order = sorted(shown, key=lambda r: (-stars[r], r.lower()))

    total = sum(len(v) for v in shown.values())
    total_stars = sum(stars[r] for r in shown)
    listed = [p for prs in shown.values() for p in prs]
    spec = load_flagships()
    # Count only what the API confirmed exists and is public, so a partial
    # render can never overstate the total.
    n_own = sum(
        1 for t in spec["tracks"] for e in t["repos"] if own.get(e["repo"])
    )

    lines: list[str] = []
    add = lines.append

    add("# Open-source record")
    add("")
    add(
        "**Two halves.** Below, the work I built and the work I landed in "
        "other people's projects. Every pull request in the second half is a "
        "commit that shipped upstream: a defect I reproduced first, the "
        "smallest fix I could defend, and the tests that pin the behaviour. "
        "Both halves are rendered from the GitHub API on a schedule, so "
        "neither can drift from what is actually public."
    )
    add("")
    add(
        "**Focus** &middot; AI agent runtimes and their memory subsystems "
        "&middot; multi-agent orchestration &middot; MCP and tool plumbing "
        "&middot; multimodal agents &middot; Python"
    )
    add("")
    add(
        "<p align=\"left\">"
        + " "
        + badge("OWN LABS", str(n_own), "bc8cff", "flask")
        + " "
        + badge("MERGED PRs", str(total), "4c8bf5", "github")
        + " "
        + badge("UPSTREAM PROJECTS", str(len(shown)), "3fb950", "package")
        + " "
        + badge("UPSTREAM STARS", stars_text(total_stars), "e3b341", "star")
        + "</p>"
    )
    add("")

    add("## Labs I built")
    add("")
    add(spec["intro"].replace("{n}", str(n_own)))
    add("")
    for track in spec["tracks"]:
        add(f"### {track['name']}")
        add("")
        add("| Repository | What it demonstrates |")
        add("| --- | --- |")
        for entry in track["repos"]:
            name = entry["repo"]
            data = own.get(name) or {}
            url = data.get("html_url") or f"https://github.com/{OWNER}/{name}"
            desc = (data.get("description") or "").replace("|", r"\|")
            hook = entry["hook"].replace("|", r"\|")
            add(f"| [{name}]({url})<br><sub>{desc}</sub> | {hook} |")
        add("")

    add("## Pull requests merged upstream")
    add("")
    add(
        f"Projects with {MIN_STARS:,}+ stars that have merged my pull requests "
        "upstream."
    )
    add("")
    add("| Project | Stars | Merged | Pull requests |")
    add("| --- | ---: | ---: | --- |")
    for full in order:
        prs = sorted(shown[full], key=lambda p: p.get("closed_at") or "")
        links = " · ".join(f"[#{p['number']}]({p['html_url']})" for p in prs)
        add(
            f"| [{full}](https://github.com/{full}) | {stars_text(stars[full])} "
            f"| {len(prs)} | {links} |"
        )
    add("")

    months = Counter(month_of(p["closed_at"]) for p in listed if p.get("closed_at"))
    add("<details>")
    add("<summary><b>Merged per month</b></summary>")
    add("")
    add("```text")
    if months:
        peak = max(months.values())
        for month in sorted(months):
            n = months[month]
            bar = "#" * max(1, round(n / peak * 40))
            add(f"{month}  {bar:<40} {n}")
    add("```")
    add("")
    add("</details>")
    add("")

    add("<details>")
    add("<summary><b>All merged pull requests</b></summary>")
    add("")
    add("| Merged | Project | Pull request |")
    add("| --- | --- | --- |")
    for pr in sorted(listed, key=lambda p: p.get("closed_at") or "", reverse=True):
        full = repo_full(pr)
        when = (pr.get("closed_at") or "")[:10]
        title = pr["title"].replace("|", "\\|")
        add(
            f"| {when} | [{full}](https://github.com/{full}) "
            f"| [#{pr['number']}]({pr['html_url']}) {title} |"
        )
    add("")
    add("</details>")
    add("")

    live: dict[str, list[dict]] = defaultdict(list)
    for pr in open_prs:
        live[repo_full(pr)].append(pr)
    if live:
        add("<details>")
        add(
            f"<summary><b>In review right now ({sum(len(v) for v in live.values())} "
            "open pull requests)</b></summary>"
        )
        add("")
        add("| Project | Open | Pull requests |")
        add("| --- | ---: | --- |")
        for full in sorted(live, key=lambda r: (-len(live[r]), r.lower())):
            prs = sorted(live[full], key=lambda p: p["number"])
            links = " · ".join(f"[#{p['number']}]({p['html_url']})" for p in prs)
            add(f"| [{full}](https://github.com/{full}) | {len(prs)} | {links} |")
        add("")
        add("</details>")
        add("")

    if excluded:
        n_ex = sum(len(v) for v in excluded.values())
        repos_word = "repository" if len(excluded) == 1 else "repositories"
        add(
            f"<sub>Plus {n_ex} merged pull request(s) in {len(excluded)} smaller "
            f"{repos_word}, below the {MIN_STARS:,} star bar of this table.</sub>"
        )
        add("")

    add("---")
    add("")
    add(
        "<sub>Rendered by "
        "[`scripts/build_readme.py`](scripts/build_readme.py) from the GitHub "
        "API &mdash; the lab table reads each repository's live description, "
        "the PR tables read the search API &mdash; and refreshed by "
        "[`.github/workflows/refresh.yml`](.github/workflows/refresh.yml) "
        f"&middot; record last changed {build_stamp()}.</sub>"
    )
    add("")
    return "\n".join(lines)


def without_stamp(text: str) -> str:
    """Drop the build timestamp so a no-op refresh does not dirty the file.

    Without this the scheduled run would commit every few hours just to move a
    clock forward, which buries the commits that mean something.
    """
    return STAMP_RE.sub("record last changed", text)


def main() -> int:
    spec = load_flagships()
    names = flagship_names(spec)
    dupes = [n for n, c in Counter(names).items() if c > 1]
    if dupes:
        raise SystemExit(f"flagships.json lists a repository twice: {dupes}")

    merged = [
        p
        for p in search(f"is:pr is:merged author:{OWNER}")
        if not repo_full(p).startswith(f"{OWNER}/")
    ]
    open_prs = [
        p
        for p in search(f"is:pr is:open author:{OWNER}")
        if not repo_full(p).startswith(f"{OWNER}/")
    ]
    repos = {repo_full(p) for p in merged}
    stars: dict[str, int] = {}
    for full in sorted(repos):
        try:
            stars[full] = stars_for(full)
        except Exception as exc:  # noqa: BLE001 - keep the page buildable
            print(f"warn: no stars for {full}: {exc}", file=sys.stderr)
            stars[full] = 0
    own, problems = fetch_own(names)
    if not merged and "--force" not in sys.argv:
        # A search that comes back empty is more likely a token or network
        # problem than a person who never merged anything: never publish it.
        problems.append("no merged pull requests found")
    if problems and "--force" not in sys.argv:
        # A curated list that no longer matches reality is worse than a stale
        # page: fail the run loudly instead of publishing a dead or private
        # link under someone's name.
        for line in problems:
            print(f"error: {line}", file=sys.stderr)
        raise SystemExit("refusing to render: the lab list does not verify")
    for line in problems:
        print(f"warn: {line}", file=sys.stderr)
    body = render(merged, open_prs, stars, own)
    print(
        f"merged={len(merged)} open={len(open_prs)} repos={len(repos)} "
        f"labs={len(own)}",
        file=sys.stderr,
    )
    if "--write" not in sys.argv:
        sys.stdout.write(body)
        return 0
    old = ""
    if os.path.exists(README):
        with open(README, encoding="utf-8") as fh:
            old = fh.read()
    if without_stamp(old) == without_stamp(body):
        print("README.md unchanged", file=sys.stderr)
        return 0
    with open(README, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    print("README.md updated", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
