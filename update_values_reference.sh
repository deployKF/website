#!/usr/bin/env bash

set -euo pipefail

THIS_SCRIPT_PATH=$(cd "$(dirname "$0")" && pwd)
cd "$THIS_SCRIPT_PATH"

# configs
VALUES_GIT_REF="fad47d82d19c8443b887b40ca93bd0a493f9e60e"
VALUES_GIT_URL="https://github.com/deployKF/deployKF/blob/${VALUES_GIT_REF}/generator/default_values.yaml"
VALUES_GIT_URL_RAW="https://raw.githubusercontent.com/deployKF/deployKF/${VALUES_GIT_REF}/generator/default_values.yaml"
VALUES_LOCAL_PATH="./.cache/default_values-${VALUES_GIT_REF}.yaml"

# download values file from github
if [ ! -f "$VALUES_LOCAL_PATH" ]; then
  wget --no-verbose -O "$VALUES_LOCAL_PATH" "$VALUES_GIT_URL_RAW"
else
  echo "File '$VALUES_LOCAL_PATH' already exists. Skipping download."
fi

# generate values csv files: `argocd`
python ./dev/generate_values_reference.py \
  --github-file-url "$VALUES_GIT_URL" \
  --input-yaml "$VALUES_LOCAL_PATH" \
  --output-csv "./content/reference/deploykf-values--{}.csv" \
  --value-include-pattern "argocd.*" \
  --value-group-level 1

# generate values csv files: `deploykf_dependencies`
python ./dev/generate_values_reference.py \
  --github-file-url "$VALUES_GIT_URL" \
  --input-yaml "$VALUES_LOCAL_PATH" \
  --output-csv "./content/reference/deploykf-values--{}.csv" \
  --value-include-pattern "deploykf_dependencies.*" \
  --value-group-level 2

# generate values csv files: `deploykf_core`
python ./dev/generate_values_reference.py \
  --github-file-url "$VALUES_GIT_URL" \
  --input-yaml "$VALUES_LOCAL_PATH" \
  --output-csv "./content/reference/deploykf-values--{}.csv" \
  --value-include-pattern "deploykf_core.*" \
  --value-group-level 2

# generate values csv files: `deploykf_opt`
python ./dev/generate_values_reference.py \
  --github-file-url "$VALUES_GIT_URL" \
  --input-yaml "$VALUES_LOCAL_PATH" \
  --output-csv "./content/reference/deploykf-values--{}.csv" \
  --value-include-pattern "deploykf_opt.*" \
  --value-group-level 2

# generate values csv files: `deploykf_tools`
python ./dev/generate_values_reference.py \
  --github-file-url "$VALUES_GIT_URL" \
  --input-yaml "$VALUES_LOCAL_PATH" \
  --output-csv "./content/reference/deploykf-values--{}.csv" \
  --value-include-pattern "deploykf_tools.*" \
  --value-group-level 2

# generate values csv files: `kubeflow_dependencies`
python ./dev/generate_values_reference.py \
  --github-file-url "$VALUES_GIT_URL" \
  --input-yaml "$VALUES_LOCAL_PATH" \
  --output-csv "./content/reference/deploykf-values--{}.csv" \
  --value-include-pattern "kubeflow_dependencies.*" \
  --value-group-level 2

# generate values csv files: `kubeflow_tools`
python ./dev/generate_values_reference.py \
  --github-file-url "$VALUES_GIT_URL" \
  --input-yaml "$VALUES_LOCAL_PATH" \
  --output-csv "./content/reference/deploykf-values--{}.csv" \
  --value-include-pattern "kubeflow_tools.*" \
  --value-group-level 2
