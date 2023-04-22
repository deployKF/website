import glob
import os

from mkdocs_table_reader_plugin.readers import read_csv


def define_env(env):
    @env.macro
    def render_values_csv_files(values_prefix, folder_path="content/reference"):
        output_lines = []

        # Find all the CSV files under `folder_path`
        file_glob = os.path.join(env.project_dir, folder_path, "deploykf-values--*.csv")
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
