import argparse
import json
import csv
from typing import List

from ruamel.yaml import YAML
import fnmatch


def flatten_yaml(yaml_data, prefix=""):
    """Recursively flatten the input YAML data and return a list of tuples (value_path, line_number, default)."""

    flattened = []
    for key, value in yaml_data.items():
        new_prefix = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict):
            flattened.extend(flatten_yaml(value, new_prefix))
        else:
            value_path = new_prefix
            line_number = yaml_data.lc.data[key][0] + 1
            default = value
            flattened.append((value_path, line_number, default))

    return flattened


def generate_csv(
    input_yaml: str,
    output_csv: str,
    value_include_pattern: str,
    value_group_level: str,
    github_file_url: str,
):
    """Generate a CSV file from a YAML file with optional filtering based on value path pattern."""

    # Load YAML data
    yaml = YAML()
    with open(input_yaml, "r") as yaml_file:
        yaml_data = yaml.load(yaml_file)

    # Flatten the YAML data
    flattened_data = flatten_yaml(yaml_data)

    # Filter the flattened data with pattern value YAML path
    filtered_data = [
        row for row in flattened_data if fnmatch.fnmatch(row[0], value_include_pattern)
    ]

    # Group by value YAML path to the defined level
    grouped_data = {}
    for value_path, line_number, default in filtered_data:
        prefix = ".".join(value_path.split(".")[:value_group_level])
        grouped_data.setdefault(prefix, []).append((value_path, line_number, default))

    # Write a CSV file for each group
    for prefix_group, data in grouped_data.items():
        with open(output_csv.format(prefix_group), "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile, lineterminator="\n")
            csv_writer.writerow(["Value", "Default"])

            for value_path, line_number, default in data:
                # Format the value path
                value_path_str = f"[`{value_path}`]({github_file_url}#L{line_number})"

                # Format the default value
                if default is None:
                    default_str = "`nil`"
                elif isinstance(default, bool):
                    default_str = "`true`" if default else "`false`"
                elif isinstance(default, str):
                    default_str = f'`"{default}"`'
                elif isinstance(default, int) or isinstance(default, float):
                    default_str = f"`{default}`"
                elif isinstance(default, dict) or isinstance(default, list):
                    default_str = f"`{json.dumps(default)}`"
                else:
                    raise ValueError(
                        f"Unexpected type for default value: {type(default)}"
                    )

                csv_writer.writerow([value_path_str, default_str])


def main():
    parser = argparse.ArgumentParser(
        description="Generate a CSV file from a YAML values file"
    )
    parser.add_argument(
        "--github-file-url",
        required=True,
        help="The URL of the YAML values file on GitHub (used for links in the CSV)",
    )
    parser.add_argument(
        "--input-yaml", required=True, help="The path of the input YAML values file"
    )
    parser.add_argument(
        "--output-csv",
        required=True,
        help="The path to write the CSV file. (Must contain '{}', which will be replaced with the value group name)",
    )
    parser.add_argument(
        "--value-include-pattern",
        required=True,
        help="A filter which must match the value for it to be included (fnmatch syntax)",
    )
    parser.add_argument(
        "--value-group-level",
        type=int,
        required=True,
        help=(
            "The level at which to group values, into separate CSV files. "
            "(E.g. if the value is 'a.b.c.d' and the group level is 2, the value will be grouped into 'a.b')"
        ),
    )

    args = parser.parse_args()

    if not args.output_csv.count("{}") == 1:
        raise ValueError("The --output-csv must contain exactly one instance of '{}'")
    if not args.value_group_level > 0:
        raise ValueError("The --value-group-level must be greater than 0")

    generate_csv(
        input_yaml=args.input_yaml,
        output_csv=args.output_csv,
        value_include_pattern=args.value_include_pattern,
        value_group_level=args.value_group_level,
        github_file_url=args.github_file_url,
    )


if __name__ == "__main__":
    main()
