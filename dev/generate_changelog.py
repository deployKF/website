import argparse
import re
import time
from functools import cmp_to_key
from typing import List, Dict

import requests


def parse_semantic_version(version_string):
    version_pattern = re.compile(
        r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
        r"(-(?P<pre_release>[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*))?"
        r"(\+(?P<build>[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*))?$"
    )
    match = version_pattern.match(version_string)
    if not match:
        raise ValueError(f"'{version_string}' is not a valid semantic version string")

    major, minor, patch = (
        int(match.group("major")),
        int(match.group("minor")),
        int(match.group("patch")),
    )
    pre_release = match.group("pre_release") or ""
    build = match.group("build") or ""
    return major, minor, patch, pre_release, build


def compare_semantic_versions(a, b):
    major_a, minor_a, patch_a, pre_release_a, build_a = parse_semantic_version(a)
    major_b, minor_b, patch_b, pre_release_b, build_b = parse_semantic_version(b)

    if major_a != major_b:
        return major_a - major_b
    if minor_a != minor_b:
        return minor_a - minor_b
    if patch_a != patch_b:
        return patch_a - patch_b

    if pre_release_a == pre_release_b:
        return 0

    if not pre_release_a:
        return 1
    if not pre_release_b:
        return -1

    pre_release_a_parts = pre_release_a.split(".")
    pre_release_b_parts = pre_release_b.split(".")

    for part_a, part_b in zip(pre_release_a_parts, pre_release_b_parts):
        if part_a == part_b:
            continue

        is_digit_a = part_a.isdigit()
        is_digit_b = part_b.isdigit()

        if is_digit_a != is_digit_b:
            return -1 if is_digit_a else 1

        if is_digit_a and is_digit_b:
            num_a = int(part_a)
            num_b = int(part_b)
            return num_a - num_b

        return (part_a > part_b) - (part_a < part_b)

    return len(pre_release_a_parts) - len(pre_release_b_parts)


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

    # Sort the releases by semantic version number
    releases.sort(
        key=lambda r: cmp_to_key(compare_semantic_versions)(r["tag_name"].lstrip("v")),
        reverse=True,
    )

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
    version = release["tag_name"].lstrip("v")
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

    return f"## [{version}]({url}) - {date}\n{content}"


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
        "--output-description", default="", help="Description for the output file"
    )
    parser.add_argument(
        "--output-admonition-type", default="info", help="The type of the output admonition"
    )
    parser.add_argument(
        "--output-admonition-title", default="", help="The title for the output admonition"
    )
    parser.add_argument(
        "--output-admonition-content", default="", help="The content for the output admonition"
    )
    parser.add_argument(
        "--output-hide-sections",
        nargs="+",
        help="MKDocs sections to hide in the output file (using page metadata)",
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
    parser.add_argument(
        "--write-version-file-path",
        default="",
        help="A path at which a text file containing the latest release version will be written",
    )

    args = parser.parse_args()

    releases = get_releases(
        args.source_repo, args.include_tag_names, args.exclude_pre_releases
    )

    if releases and args.write_version_file_path:
        with open(args.write_version_file_path, "w") as f:
            # look for the first release that is not a pre-release,
            # but if there are none, use the first release (which will be a pre-release)
            latest_version = next(
                (r["tag_name"].lstrip("v") for r in releases if not r["prerelease"]),
                releases[0]["tag_name"].lstrip("v"),
            )
            f.write(latest_version)

    changelog = []

    changelog.append("---")
    changelog.append("icon: material/script-text")
    if args.output_hide_sections:
        changelog.append("hide:")
        changelog.extend([f"  - {section}" for section in args.output_hide_sections])
    changelog.append("---")
    changelog.append("")

    changelog.append(f"# {args.output_heading}")
    changelog.append("")
    changelog.append(f"{args.output_description}")
    changelog.append("")

    if args.output_admonition_content:
        if args.output_admonition_title:
            changelog.append(f'!!! {args.output_admonition_type} "{args.output_admonition_title}"')
        else:
            changelog.append(f"!!! {args.output_admonition_type}")
        changelog.append("")
        changelog.append(f"    {args.output_admonition_content}")
        changelog.append("")

    for release in releases:
        formatted_release = format_release(release, args.include_headings)
        changelog.append(formatted_release)
        changelog.append("")

    with open(args.output_path, "w") as f:
        f.write("\n".join(changelog))


if __name__ == "__main__":
    main()
