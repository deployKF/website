import glob
import os

from mkdocs_macros.plugin import MacrosPlugin
from mkdocs_table_reader_plugin.readers import read_csv


def _render_comparison_table(comparison_data):
    output_lines = []

    # Render the table header
    output_lines.append("| Aspect |deployKF | Kubeflow Manifests |")
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
    env.macros["render_values_csv_files"] = render_values_csv_files
    env.macros["render_faq_schema"] = _render_faq_schema
    return env
