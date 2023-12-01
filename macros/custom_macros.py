import glob
import os
from typing import List

from markdown.extensions.toc import slugify
from mkdocs_macros.plugin import MacrosPlugin
from mkdocs_table_reader_plugin.readers import read_csv

# Priority to word mapping
PRIORITY_TO_WORD = {
    1: "Higher",
    2: "Medium",
    3: "Lower",
}

# Markdown in HTML
# https://python-markdown.github.io/extensions/md_in_html/
MARKDOWN = 'markdown="1"'
MARKDOWN_BLOCK = 'markdown="block"'
MARKDOWN_SPAN = 'markdown="span"'


def _html_body(
    th: List[str],
    td: List[str],
    md: bool = True,
    header_at_top: bool = False,
    th_widths: List[str] = None,
) -> str:
    """Generate an HTML table body.

    Args:
        th: List of table header cells.
        td: List of table data cells.
        md: Enable markdown in cells.

    Returns:
        The HTML for the table row.
    """
    output = ""

    if md:
        _md = MARKDOWN_SPAN
    else:
        _md = ""

    # generate the table row
    if header_at_top:
        # add header
        output += f"<thead {_md}>"
        output += f"<tr {_md}>"
        for index, cell in enumerate(th):
            if th_widths:
                output += f"<th {_md} width='{th_widths[index]}'>{cell}</th>"
            else:
                output += f"<th {_md}>{cell}</th>"
        output += "</tr>"
        output += "</thead>"

        # add body
        output += f"<tbody {_md}>"
        output += f"<tr {_md}>"
        for cell in td:
            output += f"<td {_md}>{cell}</td>"
        output += "</tr>"
        output += "</tbody>"
    else:
        # add body
        output += f"<tbody {_md}>"
        output += f"<tr {_md}>"
        for cell in th:
            output += f"<th {_md}>{cell}</th>"
        for cell in td:
            output += f"<td {_md}>{cell}</td>"
        output += "</tr>"
        output += "</tbody>"

    return output


def define_env(env: MacrosPlugin):
    @env.macro
    def render_comparison_table(comparison_data):
        output_lines = []

        # For each aspect, render a table
        for row in comparison_data:
            aspect = row["aspect"]

            # Add header for the aspect
            output_lines.append(f"### {aspect}")
            output_lines.append("")

            # List of deploykf items
            dkf_items = [f"<p>{item}</p>" for item in row["deploykf"]]
            dkf_str = " ".join(dkf_items)

            # List of kubeflow manifests items
            kfm_items = [f"<p>{item}</p>" for item in row["kubeflow_manifests"]]
            kfm_str = " ".join(kfm_items)

            # Render comparison table
            output_lines.append(f"<div {MARKDOWN_BLOCK} class='comparison-table'>")
            output_lines.append(f"<table {MARKDOWN_SPAN}>")
            output_lines.append(
                _html_body(
                    [
                        ":custom-deploykf-color: deployKF",
                        ":custom-kubeflow-color: Kubeflow Manifests",
                    ],
                    [dkf_str, kfm_str],
                    header_at_top=True,
                    th_widths=["50%", "50%"],
                )
            )
            output_lines.append(f"</table>")
            output_lines.append(f"</div>")

        return "\n".join(output_lines)

    @env.macro
    def render_current_tools_index(current_tools_data):
        output_lines = []

        # Render the table header
        output_lines.append(
            "| Name<br><small>(Click for Details)</small> | Purpose | Since deployKF |"
        )
        output_lines.append("| --- | --- | --- |")

        # Render the table body
        for row in current_tools_data:
            tool_name = row["name"]
            tool_link = f"[__{tool_name}__](#{slugify(tool_name, '-')})"
            tool_purpose = row["purpose"]
            dkf_version = row["deploykf_version"]
            output_lines.append(f"| {tool_link} | {tool_purpose} | `{dkf_version}` |")

        return "\n".join(output_lines)

    @env.macro
    def render_current_tools_details(current_tools_data):
        output_lines = []

        for row in current_tools_data:
            tool_name = row["name"]
            dkf_values = row["deploykf_values"]
            dkf_values_link = f"[`{dkf_values}`](../reference/deploykf-values.md#{slugify(dkf_values, '-')})"

            if row["github_repo"]:
                upstream_repo_link = (
                    f"[`{row['github_repo']}`](https://github.com/{row['github_repo']})"
                )
            else:
                upstream_repo_link = "N/A"

            if row["docs_url"]:
                upstream_docs_link = f"[Documentation]({row['docs_url']})"
            else:
                upstream_docs_link = "N/A"

            # Render tool header
            output_lines.append(f"### {tool_name}")
            output_lines.append("")

            # Render introduction
            output_lines.append(row["introduction"])
            output_lines.append("")

            # Render details table
            output_lines.append(f"<table {MARKDOWN_SPAN}>")
            output_lines.append(_html_body(["Purpose"], [row["purpose"]]))
            output_lines.append(_html_body(["Maintainer"], [row["maintainer"]]))
            output_lines.append(
                _html_body(["Documentation"], [upstream_docs_link]),
            )
            output_lines.append(
                _html_body(["Source Code"], [upstream_repo_link]),
            )
            output_lines.append(_html_body(["deployKF Configs"], [dkf_values_link]))
            output_lines.append(
                _html_body(["Since deployKF"], [f'`{row["deploykf_version"]}`'])
            )
            output_lines.append(f"</table>")

            # Render tool description
            tool_description = row["description"]
            if tool_description:
                output_lines.append(f'!!! value ""')
                for description_line in row["description"].splitlines():
                    output_lines.append(f"     {description_line}")
                output_lines.append("")

            # Render tool footnote
            tool_footnote = row["footnote"]
            if tool_footnote:
                output_lines.append(tool_footnote)
                output_lines.append("")

        return "\n".join(output_lines)

    @env.macro
    def render_planned_tools_index(planned_tools_data):
        output_lines = []

        current_priority = None

        # Loop through the tools in priority order
        for row in sorted(
            planned_tools_data,
            key=lambda t: (t["deploykf_priority"], t["purpose"], t["name"]),
        ):
            tool_priority = row["deploykf_priority"]
            tool_priority_word = PRIORITY_TO_WORD[tool_priority]

            # If the priority has changed, start a new section and table
            if tool_priority != current_priority:
                current_priority = tool_priority
                output_lines.append("")
                output_lines.append(f"### {tool_priority_word} Priority")
                output_lines.append("")
                output_lines.append(
                    "| Name<br><small>(Click for Details)</small> | Purpose |"
                )
                output_lines.append("| --- | --- |")

            tool_name = row["name"]
            tool_link = f"[__{tool_name}__](#{slugify(tool_name, '-')})"
            tool_purpose = row["purpose"]
            output_lines.append(f"| {tool_link} | {tool_purpose} |")

        return "\n".join(output_lines)

    @env.macro
    def render_planned_tools_details(planned_tools_data):
        output_lines = []

        for row in sorted(
            planned_tools_data,
            key=lambda t: (t["deploykf_priority"], t["purpose"], t["name"]),
        ):
            tool_name = row["name"]

            if row["github_repo"]:
                upstream_repo_link = (
                    f"[`{row['github_repo']}`](https://github.com/{row['github_repo']})"
                )
            else:
                upstream_repo_link = "N/A"

            if row["docs_url"]:
                upstream_docs_link = f"[Documentation]({row['docs_url']})"
            else:
                upstream_docs_link = "N/A"

            # Render tool header
            output_lines.append(f"### {tool_name}")
            output_lines.append("")

            # Render introduction
            output_lines.append(row["introduction"])
            output_lines.append("")

            # Render details table
            output_lines.append(f"<table {MARKDOWN_SPAN}>")
            output_lines.append(_html_body(["Purpose"], [row["purpose"]]))
            output_lines.append(_html_body(["Maintainer"], [row["maintainer"]]))
            output_lines.append(
                _html_body(
                    ["Documentation"],
                    [upstream_docs_link],
                )
            )
            output_lines.append(
                _html_body(
                    ["Source Code"],
                    [upstream_repo_link],
                )
            )
            output_lines.append(
                _html_body(
                    ["Roadmap Priority"],
                    [PRIORITY_TO_WORD[row["deploykf_priority"]]],
                )
            )
            output_lines.append(f"</table>")

            # Render tool description
            tool_description = row["description"]
            if tool_description:
                output_lines.append(f'!!! value ""')
                for description_line in row["description"].splitlines():
                    output_lines.append(f"     {description_line}")
                output_lines.append("")

            # Render tool footnote
            tool_footnote = row["footnote"]
            if tool_footnote:
                output_lines.append(tool_footnote)
                output_lines.append("")

        return "\n".join(output_lines)

    @env.macro
    def render_values_csv_files(values_prefix):
        # get folder path from env
        folder_path = os.path.join(env.project_dir, "content/reference")

        output_lines = []

        # Find all the CSV files under `folder_path`
        file_glob = os.path.join(folder_path, "deploykf-values--*.csv")
        files = glob.glob(file_glob)

        # Create a section for each CSV file
        for file in files:
            # Extract the section name from the file name
            # NOTE: the file names are in the format `deploykf-values--<VALUES_PREFIX>.csv`
            section_name = (
                os.path.basename(file)
                .replace("deploykf-values--", "")
                .replace(".csv", "")
            )

            # Skip files that don't match the values prefix
            if values_prefix:
                if not section_name.startswith(values_prefix):
                    continue

            # Render the CSV file using the `read_csv` macro from the `mkdocs-table-reader-plugin`
            table_md = read_csv(file)

            # Add a section for this CSV to the output
            output_lines.append(f"### `{section_name}`")
            output_lines.append("")
            output_lines.append(table_md)
            output_lines.append("")

        return "\n".join(output_lines)

    @env.macro
    def render_faq_schema(faq_schema):
        output_lines = []

        for faq_entry in faq_schema:
            question = faq_entry["question"]
            if faq_entry.get("admonition_type", False):
                question_type = faq_entry.get("admonition_type")
            elif faq_entry.get("highlight_answer", False):
                question_type = "question"
            else:
                question_type = "question_secondary"

            output_lines.append("")
            if faq_entry.get("pre_expand_answer", False):
                output_lines.append(f'???+ {question_type} "{question}"')
            else:
                output_lines.append(f'??? {question_type} "{question}"')

            output_lines.append(f"    ###### {question}")
            output_lines.append("")

            for answer_line in faq_entry["answer"].splitlines():
                output_lines.append(f"    {answer_line}")
            output_lines.append("")

        return "\n".join(output_lines)

    return env
