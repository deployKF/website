import argparse
import re
import time
from typing import List, Dict

import requests


def get_releases(
    source_repo: str, tag_name_regex: str, exclude_pre_releases: bool
) -> List[dict]:
    url = f"https://api.github.com/repos/{source_repo}/releases"
    releases = []
    page = 1

    while True:
        params = {"page": page, "per_page": 100}
        response = requests.get(url, params=params)

        # Check for rate limiting (github uses status code 403)
        # https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#exceeding-the-rate-limit
        while response.status_code == 403:
            reset_timestamp = int(response.headers.get("X-RateLimit-Reset", 0))
            sleep_duration = max(reset_timestamp - time.time(), 0)
            print(
                f"Rate limited. Sleeping for {sleep_duration} seconds (until 'X-RateLimit-Reset')..."
            )
            time.sleep(sleep_duration)

            # Retry the request after sleeping
            response = requests.get(url, params=params)

        response.raise_for_status()
        data = response.json()

        # If no data is returned, it means you have reached the last page
        if not data:
            break

        for release in data:
            if exclude_pre_releases and release["prerelease"]:
                continue

            if not re.fullmatch(tag_name_regex, release["tag_name"]):
                continue

            releases.append(release)

        # If less than 100 releases are returned, it means you have reached the last page
        if len(data) < 100:
            break

        page += 1

    return releases


def filter_content(content: str, include_headings: List[str]) -> str:
    """
    Filter release content to only include the content under specified headings.
     - The headings are expected to be H3 (##) in the release description.
     - The content of a heading ends when the next heading is encountered OR two newlines are encountered.
    """
    lines = content.splitlines()
    filtered_lines = []

    last_line = ""
    include_section = False
    for line in lines:
        if line.startswith("# "):
            include_section = False
        elif line.startswith("## "):
            include_section = False
        elif line.startswith("### "):
            heading = line[4:]
            if heading in include_headings:
                # add a newline before this heading
                filtered_lines.append("")
                filtered_lines.append(line)
                include_section = True
            else:
                include_section = False
        elif include_section:
            if line.strip() == "" and last_line.strip() == "":
                include_section = False
            else:
                filtered_lines.append(line)

        last_line = line

    return "\n".join(filtered_lines)


def format_release(release: Dict[str, str], include_headings: List[str]) -> str:
    version = release["tag_name"]
    date = release["published_at"][:10]
    url = release["html_url"]
    content = filter_content(release["body"], include_headings)

    # Replace links to pull requests and issues with markdown links
    escaped_github_url = re.escape(f"https://github.com")
    content = re.sub(
        rf"{escaped_github_url}/([^/]+)/([^/]+)/(pull|issues)/(\d+)",
        r"[#\4](https://github.com/\1/\2/\3/\4)",
        content,
    )

    # Replace @mentions with markdown links
    content = re.sub(r"@(\w+)", r"[@\1](https://github.com/\1)", content)

    return f"\n## [{version}]({url}) - {date}\n{content}"


def main():
    parser = argparse.ArgumentParser(
        description="Generate markdown changelog from GitHub releases."
    )
    parser.add_argument(
        "--source-repo", required=True, help="GitHub repository to read releases from"
    )
    parser.add_argument(
        "--output-path",
        required=True,
        help="Output path for the changelog markdown file",
    )
    parser.add_argument(
        "--output-heading", default="Changelog", help="H1 heading for the output file"
    )
    parser.add_argument(
        "--include-headings",
        nargs="+",
        required=True,
        help="H3 headings from release descriptions to include",
    )
    parser.add_argument(
        "--include-tag-names",
        default=".*",
        help="Pattern to match release tag names for inclusion",
    )
    parser.add_argument(
        "--exclude-pre-releases",
        action="store_true",
        help="Exclude prerelease GitHub releases",
    )

    args = parser.parse_args()

    releases = get_releases(
        args.source_repo, args.include_tag_names, args.exclude_pre_releases
    )
    changelog = [f"# {args.output_heading}\n"]

    for release in releases:
        formatted_release = format_release(release, args.include_headings)
        changelog.append(formatted_release)

    with open(args.output_path, "w") as f:
        f.write("\n".join(changelog))


if __name__ == "__main__":
    main()
