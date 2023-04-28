import glob
import os
import re

import markdown
from mkdocs_macros.plugin import MacrosPlugin
from mkdocs_table_reader_plugin.readers import read_csv


def __md_to_html(value, single_line=True):
    html_text = markdown.markdown(value, extensions=["extra", "sane_lists"])
    if single_line:
        html_text = re.sub(r"\s+", " ", html_text).strip()
    return html_text


def __gen_md_anchor(title):
    # Convert title to lowercase
    anchor = title.lower()

    # Replace special characters with an empty string, except for hyphens, underscores, and whitespace
    anchor = re.sub(r"[^\w\s-]", "", anchor)

    # Replace consecutive spaces with single space
    anchor = re.sub(r"\s+", " ", anchor)

    # Replace whitespace with hyphens
    anchor = re.sub(r"\s", "-", anchor)

    # Remove hyphens at the beginning and end of the string
    anchor = anchor.strip("-")

    return anchor


def _render_comparison_table(comparison_data):
    output_lines = []

    # Render the table header
    output_lines.append("| Aspect | deployKF | Kubeflow Manifests |")
    output_lines.append("| --- | --- | --- |")

    # Render the table body
    for row in comparison_data:
        aspect = row["aspect"]
        dkf_items = [f"<li>{item}</li>" for item in row["deploykf"]]
        dkf_str = f"<ul>{''.join(dkf_items)}</ul>"
        kfm_items = [f"<li>{item}</li>" for item in row["kubeflow_manifests"]]
        kfm_str = f"<ul>{''.join(kfm_items)}</ul>"
        output_lines.append(f"| {aspect} | {dkf_str} | {kfm_str} |")

    return "\n".join(output_lines)


def _render_current_tools_index(current_tools_data):
    output_lines = []

    # Render the table header
    output_lines.append("| Tool | Purpose | deployKF Version |")
    output_lines.append("| --- | --- | --- |")

    # Render the table body
    for row in current_tools_data:
        tool_name = row["name"]
        tool_link = f"[{tool_name}](#{__gen_md_anchor(tool_name)})"
        tool_purpose = row["purpose"]
        dkf_version = row["deploykf_version"]
        output_lines.append(f"| {tool_link} | {tool_purpose} | `>= {dkf_version}` |")

    return "\n".join(output_lines)


def _render_current_tools_details(current_tools_data):
    output_lines = []

    for row in current_tools_data:
        tool_name = row["name"]
        dkf_values = row["deploykf_values"]
        dkf_values_link = f"[`{dkf_values}`](/reference/deploykf-values/#{__gen_md_anchor(dkf_values)})"

        # Render tool header
        output_lines.append(f"## {tool_name}")
        output_lines.append("")

        # Render tool description header
        output_lines.append("### Tool Description:")
        output_lines.append("")

        # Render tool description
        output_lines.append(row["description"])
        output_lines.append("")

        # Render tool details header
        output_lines.append("### Tool Details:")
        output_lines.append("")

        # Render details table
        output_lines.append(f"| Name | {tool_name} |")
        output_lines.append("| --- | --- |")
        output_lines.append(f"| Owner | {row['owner']} |")
        output_lines.append(f"| Purpose | {row['purpose']} |")
        output_lines.append(f"| deployKF Version | `>= {row['deploykf_version']}` |")
        output_lines.append(f"| deployKF Values | {dkf_values_link} |")
        output_lines.append(
            f"| Upstream Repo | [`{row['github_repo']}`](https://github.com/{row['github_repo']}) |"
        )
        output_lines.append(f"| Upstream Docs | [Documentation]({row['docs_url']}) |")
        output_lines.append("")

    return "\n".join(output_lines)


def _render_planned_tools_index(planned_tools_data):
    output_lines = []

    # Render the table header
    output_lines.append("| Tool | Purpose | deployKF Priority |")
    output_lines.append("| --- | --- | --- |")

    # Render the table body
    for row in sorted(
        planned_tools_data,
        key=lambda t: (t["deploykf_priority"], t["purpose"], t["name"]),
    ):
        tool_name = row["name"]
        tool_link = f"[{tool_name}](#{__gen_md_anchor(tool_name)})"
        tool_purpose = row["purpose"]
        dkf_priority = row["deploykf_priority"]
        output_lines.append(f"| {tool_link} | {tool_purpose} | `P{dkf_priority}` |")

    return "\n".join(output_lines)


def _render_planned_tools_details(planned_tools_data):
    output_lines = []

    for row in sorted(
        planned_tools_data,
        key=lambda t: (t["deploykf_priority"], t["purpose"], t["name"]),
    ):
        tool_name = row["name"]

        # Render tool header
        output_lines.append(f"## {tool_name}")
        output_lines.append("")

        # Render tool description header
        output_lines.append("### Tool Description:")
        output_lines.append("")

        # Render tool description
        output_lines.append(row["description"])
        output_lines.append("")

        # Render tool details header
        output_lines.append("### Tool Details:")
        output_lines.append("")

        # Render details table
        output_lines.append(f"| Name | {tool_name} |")
        output_lines.append("| --- | --- |")
        output_lines.append(f"| Owner | {row['owner']} |")
        output_lines.append(f"| Purpose | {row['purpose']} |")
        output_lines.append(f"| deployKF Priority | `P{row['deploykf_priority']}` |")
        output_lines.append(
            f"| Upstream Repo | [`{row['github_repo']}`](https://github.com/{row['github_repo']}) |"
        )
        output_lines.append(f"| Upstream Docs | [Documentation]({row['docs_url']}) |")
        output_lines.append("")

    return "\n".join(output_lines)


def _render_faq_schema(faq_schema):
    output_lines = []

    for faq_entry in faq_schema:
        output_lines.append(f"## {faq_entry['question']}")
        output_lines.append("")

        if faq_entry.get("pre_expand_answer", False):
            output_lines.append('???+ question "Answer"')
        else:
            output_lines.append('??? question "Answer"')

        output_lines.append("")
        for answer_line in faq_entry["answer"].splitlines():
            output_lines.append(f"    {answer_line}")
        output_lines.append("")

    return "\n".join(output_lines)


def _render_values_csv_files(values_prefix, folder_path):
    output_lines = []

    # Find all the CSV files under `folder_path`
    file_glob = os.path.join(folder_path, "deploykf-values--*.csv")
    files = glob.glob(file_glob)

    # Create a section for each CSV file
    for file in files:
        # Extract the section name from the file name
        # NOTE: the file names are in the format `deploykf-values--<VALUES_PREFIX>.csv`
        section_name = (
            os.path.basename(file).replace("deploykf-values--", "").replace(".csv", "")
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


def define_env(env: MacrosPlugin):
    # we define a wrapper here to access `env.project_dir
    def render_values_csv_files(values_prefix):
        folder_path = os.path.join(env.project_dir, "content/reference")
        return _render_values_csv_files(values_prefix, folder_path)

    env.macros["render_comparison_table"] = _render_comparison_table
    env.macros["render_current_tools_index"] = _render_current_tools_index
    env.macros["render_current_tools_details"] = _render_current_tools_details
    env.macros["render_planned_tools_index"] = _render_planned_tools_index
    env.macros["render_planned_tools_details"] = _render_planned_tools_details
    env.macros["render_values_csv_files"] = render_values_csv_files
    env.macros["render_faq_schema"] = _render_faq_schema
    return env
