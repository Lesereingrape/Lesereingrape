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
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict

OWNER = (
    os.environ.get("PROFILE_OWNER")
    or os.environ.get("GITHUB_REPOSITORY_OWNER")
    or "Lesereingrape"
)
MIN_STARS = int(os.environ.get("MIN_STARS", "10000"))
API = "https://api.github.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
FLAGSHIPS = os.path.join(ROOT, "scripts", "flagships.json")
STAMP_RE = re.compile(r"record last changed \d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC")

# Organizations that are community or academic groups rather than companies.
# Individual maintainer accounts need no entry here: the API already reports
# them as owner type "User". This list only carries the ones that hide behind
# an organization login, and it is kept because the profile leads with companies.
COMMUNITY_OWNERS = {
    "AstrBotDevs",
    "HKUDS",
    "StarTrail-org",
}

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
    """Fetch an API document, retrying a dropped connection.

    A connection that dies mid-handshake is a network flake, not a missing
    repository. Without a retry one flake reads as "no metadata", which sinks a
    real company project to the bottom of the page and understates the totals.
    """
    for attempt in range(3):
        try:
            return _get(url)
        except urllib.error.HTTPError:
            # A status code is an answer; only a lost connection is retried.
            raise
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == 2:
                raise
            print(f"retry {attempt + 1}: {url}: {exc}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    raise AssertionError("unreachable")


def _get(url: str):
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


REPOS: dict[str, dict] = {}


def repo_doc(full: str) -> dict:
    """Read an upstream repository once per build.

    The star count and the owner type both steer the layout, so both are taken
    from the same response: a repository cannot be grouped by one snapshot and
    labelled by another.
    """
    if full not in REPOS:
        REPOS[full] = get(f"{API}/repos/{full}")
    return REPOS[full]


def stars_for(full: str) -> int:
    return int(repo_doc(full).get("stargazers_count") or 0)


def solo_for(full: str) -> bool:
    """True when a repository belongs to a person or a community group.

    The owner type is read from the API rather than inferred from the login, so
    the page can claim "company-backed" without a hand-kept list going stale.
    """
    doc = repo_doc(full)
    if (doc.get("owner") or {}).get("type") != "Organization":
        return True
    return full.split("/", 1)[0] in COMMUNITY_OWNERS


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


def pr_table(
    repos: dict[str, list[dict]], stars: dict[str, int], order: list[str]
) -> list[str]:
    rows = ["| Project | Stars | Merged | Pull requests |", "| --- | ---: | ---: | --- |"]
    for full in order:
        prs = sorted(repos[full], key=lambda p: p.get("closed_at") or "")
        links = " · ".join(f"[#{p['number']}]({p['html_url']})" for p in prs)
        rows.append(
            f"| [{full}](https://github.com/{full}) | {stars_text(stars[full])} "
            f"| {len(prs)} | {links} |"
        )
    return rows


def open_pr_table(repos: dict[str, list[dict]], stars: dict[str, int], order: list[str]) -> list[str]:
    rows = ["| Project | Stars | Open | Pull requests |", "| --- | ---: | ---: | --- |"]
    for full in order:
        prs = sorted(repos[full], key=lambda p: p["number"])
        links = " · ".join(f"[#{p['number']}]({p['html_url']})" for p in prs)
        rows.append(
            f"| [{full}](https://github.com/{full}) | {stars_text(stars[full])} "
            f"| {len(prs)} | {links} |"
        )
    return rows


def render(
    merged: list[dict],
    open_prs: list[dict],
    stars: dict[str, int],
    own: dict,
    solo: set[str],
) -> str:
    by_repo: dict[str, list[dict]] = defaultdict(list)
    for pr in merged:
        by_repo[repo_full(pr)].append(pr)

    # Two independent facts decide where a repository sits: who owns it, and how
    # much traffic it carries. A known project owned by a single maintainer is
    # still shown, just below the companies; the star bar only controls whether
    # a group is open by default.
    big = {r: v for r, v in by_repo.items() if stars.get(r, 0) >= MIN_STARS}
    small = {r: v for r, v in by_repo.items() if r not in big}
    company = {r: v for r, v in big.items() if r not in solo}
    community = {r: v for r, v in big.items() if r in solo}

    def by_stars(repos: dict[str, list[dict]]) -> list[str]:
        return sorted(repos, key=lambda r: (-stars[r], r.lower()))

    def group(
        repos: dict[str, list[dict]],
        title: str,
        note: str,
        table=pr_table,
    ) -> None:
        add("<details>")
        add(
            f"<summary><b>{title} ({sum(len(v) for v in repos.values())} pull "
            f"request(s) in {len(repos)} project(s))</b></summary>"
        )
        add("")
        add(note)
        add("")
        lines.extend(table(repos, stars, by_stars(repos)))
        add("")
        add("</details>")
        add("")

    n_all = sum(len(v) for v in by_repo.values())
    total_stars = sum(stars[r] for r in big)
    # Every merged PR is listed, including the collapsed groups, so the summary
    # rows cannot understate the record.
    listed = [p for prs in by_repo.values() for p in prs]
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
        + badge("MERGED PRs", str(n_all), "4c8bf5", "github")
        + " "
        + badge("COMPANY PROJECTS", str(len(company)), "3fb950", "building")
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

    add("## Merged into company-backed projects")
    add("")
    add(
        f"Repositories run by a company or product organisation, each with "
        f"{MIN_STARS:,}+ stars, that have merged my pull requests upstream."
    )
    add("")
    if company:
        lines.extend(pr_table(company, stars, by_stars(company)))
    else:
        add("No company-backed merge has reached this bar yet.")
    add("")

    if community:
        group(
            community,
            "Merged into community and individual-maintainer projects",
            f"Also {MIN_STARS:,}+ stars, but owned by a solo maintainer or an "
            "academic / community group rather than a company.",
        )

    if small:
        group(
            small,
            f"Merged into projects under {MIN_STARS:,} stars",
            f"Real merges, below the {MIN_STARS:,} star bar of the tables above.",
        )

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
    withheld = 0
    for pr in open_prs:
        # A draft is a pull request I am not asking anyone to review, so it stays
        # off the table and the heading says how many were left out.
        if pr.get("draft"):
            withheld += 1
            continue
        live[repo_full(pr)].append(pr)
    if live:
        shown = sum(len(v) for v in live.values())
        review_big = {r: v for r, v in live.items() if stars.get(r, 0) >= MIN_STARS}
        review_company = {r: v for r, v in review_big.items() if r not in solo}
        review_community = {r: v for r, v in review_big.items() if r in solo}
        review_small = {r: v for r, v in live.items() if r not in review_big}

        add("## In review right now")
        add("")
        add(
            f"{shown} open pull request{'s' if shown != 1 else ''} of mine are "
            "waiting on a maintainer"
            + (f" ({withheld} more held back as draft)" if withheld else "")
            + f". Company-backed projects above {MIN_STARS:,} stars come first; "
            "every other open pull request stays listed, just below them."
        )
        add("")
        if review_company:
            lines.extend(open_pr_table(review_company, stars, by_stars(review_company)))
        else:
            add("No open pull request sits in a company-backed project yet.")
        add("")

        if review_community:
            group(
                review_community,
                "Open in community and individual-maintainer projects",
                f"Also {MIN_STARS:,}+ stars, but owned by a solo maintainer or an "
                "academic / community group rather than a company.",
                table=open_pr_table,
            )
        if review_small:
            group(
                review_small,
                f"Open in projects under {MIN_STARS:,} stars",
                "Earlier work still in review, below the "
                f"{MIN_STARS:,} star bar of the tables above.",
                table=open_pr_table,
            )

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
    # Open pull requests are tiered by the same two facts as merged ones, so the
    # projects still waiting upstream have to be classified too.
    repos = {repo_full(p) for p in merged} | {repo_full(p) for p in open_prs}
    stars: dict[str, int] = {}
    # A repository whose metadata cannot be read stays out of the company table:
    # a failed lookup must never buy a project a prominent listing.
    solo: set[str] = set(repos)
    for full in sorted(repos):
        try:
            stars[full] = stars_for(full)
            if not solo_for(full):
                solo.discard(full)
        except Exception as exc:  # noqa: BLE001 - keep the page buildable
            print(f"warn: no metadata for {full}: {exc}", file=sys.stderr)
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
    body = render(merged, open_prs, stars, own, solo)
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
