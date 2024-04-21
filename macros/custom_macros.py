import glob
import os
import textwrap
from typing import List, Union

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
    tr: Union[List[str], List[List[str]]],
    md: bool = True,
    header_at_top: bool = False,
    th_widths: List[str] = None,
) -> str:
    """Generate an HTML table body.

    Args:
        th: List of table header cells.
        tr: List of table rows, each being a list of cell values.
            OR: a list of cells if `header_at_top` is False.
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
        # require `tr` to be a list of lists
        if not isinstance(tr[0], list):
            raise ValueError("`header_at_top` is True, `tr` must be a list of lists")

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
        for td in tr:
            output += f"<tr {_md}>"
            for cell in td:
                output += f"<td {_md}>{cell}</td>"
            output += "</tr>"
        output += "</tbody>"
    else:
        # require `tr` to be a list of cells
        if not isinstance(tr[0], str):
            raise ValueError("`header_at_top` is False, `tr` must be a list of cells")
        else:
            td = tr

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


def _bool_to_md(value: bool) -> str:
    """Convert a boolean to a markdown checkmark or cross icon."""
    if value:
        return "<span class='comparison-icon comparison-icon--yes'> :fontawesome-solid-square-check: </span>"
    else:
        return "<span class='comparison-icon comparison-icon--no'> :fontawesome-solid-square-xmark: </span>"


def define_env(env: MacrosPlugin):
    @env.macro
    def render_comparison_table(comparison_data):
        output_lines = []

        # For each aspect, render a table
        for section in comparison_data:
            aspect = section["aspect"]

            # Add header for the aspect
            output_lines.append(f"### Area: __{aspect}__")
            output_lines.append("")

            feature_list = []
            dkf_list = []
            kfm_list = []

            for feature in section["features"]:
                feature_name = feature["name"]
                feature_list.append(f"{feature_name}")

                dkf_data = feature["deploykf"]
                dkf_feat_has = dkf_data["has_feature"]
                dkf_feat_desc = dkf_data["description"].replace("\n", "<br>")
                dkf_list.append(
                    f"{_bool_to_md(dkf_feat_has)}<hr><small>{dkf_feat_desc}</small>"
                )

                kfm_data = feature["kubeflow_manifests"]
                kfm_feat_has = kfm_data["has_feature"]
                kfm_feat_desc = kfm_data["description"].replace("\n", "<br>")
                kfm_list.append(
                    f"{_bool_to_md(kfm_feat_has)}<hr><small>{kfm_feat_desc}</small>"
                )

            # Render comparison table
            output_lines.append(f"<div {MARKDOWN_BLOCK} class='comparison-table'>")
            output_lines.append(f"<table {MARKDOWN_SPAN}>")
            output_lines.append(
                _html_body(
                    [
                        "Feature",
                        ":custom-deploykf-color: deployKF",
                        ":custom-kubeflow-color: Kubeflow Manifests",
                    ],
                    [[f, d, k] for f, d, k in zip(feature_list, dkf_list, kfm_list)],
                    header_at_top=True,
                    th_widths=["30%", "35%", "35%"],
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

            # Render admonition wrapper
            output_lines.append(f'??? abstract "Details - _{tool_name}_"')
            output_lines.append("")

            # NOTE: we create a separate list here, so we can indent the admonition content
            admonition_content = []

            # Render tool header
            admonition_content.append(f"#### {tool_name}")
            admonition_content.append("")

            # Render details table
            admonition_content.append(f"<table {MARKDOWN_SPAN}>")
            admonition_content.append(_html_body(["Purpose"], [row["purpose"]]))
            admonition_content.append(_html_body(["Maintainer"], [row["maintainer"]]))
            admonition_content.append(
                _html_body(["Documentation"], [upstream_docs_link]),
            )
            admonition_content.append(
                _html_body(["Source Code"], [upstream_repo_link]),
            )
            admonition_content.append(
                _html_body(["deployKF Configs"], [dkf_values_link])
            )
            admonition_content.append(
                _html_body(["Since deployKF"], [f'`{row["deploykf_version"]}`'])
            )
            admonition_content.append(f"</table>")

            # Render introduction
            admonition_content.append(row["introduction"])
            admonition_content.append("")

            # Divider
            admonition_content.append("")
            admonition_content.append("---")
            admonition_content.append("")

            # Render tool description
            tool_description = row["description"]
            if tool_description:
                for description_line in row["description"].splitlines():
                    admonition_content.append(description_line)
                admonition_content.append("")

            # Render tool footnote
            tool_footnote = row["footnote"]
            if tool_footnote:
                admonition_content.append(tool_footnote)
                admonition_content.append("")

            # Add the admonition content to the output
            for line_content in admonition_content:
                output_lines.append(textwrap.indent(line_content, "    "))

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

            # Render admonition wrapper
            output_lines.append(f'??? abstract "Details - _{tool_name}_"')
            output_lines.append("")

            # NOTE: we create a separate list here, so we can indent the admonition content
            admonition_content = []

            # Render tool header
            admonition_content.append(f"#### {tool_name}")
            admonition_content.append("")

            # Render details table
            admonition_content.append(f"<table {MARKDOWN_SPAN}>")
            admonition_content.append(_html_body(["Purpose"], [row["purpose"]]))
            admonition_content.append(_html_body(["Maintainer"], [row["maintainer"]]))
            admonition_content.append(
                _html_body(
                    ["Documentation"],
                    [upstream_docs_link],
                )
            )
            admonition_content.append(
                _html_body(
                    ["Source Code"],
                    [upstream_repo_link],
                )
            )
            admonition_content.append(
                _html_body(
                    ["Roadmap Priority"],
                    [PRIORITY_TO_WORD[row["deploykf_priority"]]],
                )
            )
            admonition_content.append(f"</table>")

            # Render introduction
            admonition_content.append(row["introduction"])
            admonition_content.append("")

            # Divider
            admonition_content.append("")
            admonition_content.append("---")
            admonition_content.append("")

            # Render tool description
            tool_description = row["description"]
            if tool_description:
                for description_line in row["description"].splitlines():
                    admonition_content.append(description_line)
                admonition_content.append("")

            # Render tool footnote
            tool_footnote = row["footnote"]
            if tool_footnote:
                admonition_content.append(tool_footnote)
                admonition_content.append("")

            # Add the admonition content to the output
            for line_content in admonition_content:
                output_lines.append(textwrap.indent(line_content, "    "))

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

            # Render admonition wrapper
            output_lines.append(f'??? value "`{section_name}`"')
            output_lines.append("")

            # NOTE: we create a separate list here, so we can indent the admonition content
            admonition_content = []

            # Add a section for this CSV to the output
            admonition_content.append(f"#### `{section_name}`")
            admonition_content.append("")
            admonition_content.append(table_md)
            admonition_content.append("")

            # Add the admonition content to the output
            for line_content in admonition_content:
                output_lines.append(textwrap.indent(line_content, "    "))

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
