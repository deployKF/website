#!/usr/bin/env bash

set -euo pipefail

THIS_SCRIPT_PATH=$(cd "$(dirname "$0")" && pwd)
cd "$THIS_SCRIPT_PATH"

# generate the changelog for the deployKF/deployKF repo (excluding pre-releases)
python ./dev/generate_changelog.py \
  --source-repo deployKF/deployKF \
  --output-path ./content/releases/changelogs/changelog-deploykf.md \
  --output-heading "Changelog for deployKF" \
  --include-headings "Significant Changes" "New Features" "Improvements" "Bug Fixes" "Documentation" "Miscellaneous" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --exclude-pre-releases

# generate the full changelog for the deployKF/deployKF repo
python ./dev/generate_changelog.py \
  --source-repo deployKF/deployKF \
  --output-path ./content/releases/changelogs/full-changelog-deploykf.md \
  --output-heading "Full changelog for deployKF" \
  --include-headings "Significant Changes" "New Features" "Improvements" "Bug Fixes" "Documentation" "Miscellaneous" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?'

# generate the changelog for the deployKF/cli repo (excluding pre-releases)
python ./dev/generate_changelog.py \
  --source-repo deployKF/cli \
  --output-path ./content/releases/changelogs/changelog-cli.md \
  --output-heading "Changelog for CLI" \
  --include-headings "Significant Changes" "New Features" "Improvements" "Bug Fixes" "Documentation" "Miscellaneous" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --exclude-pre-releases

# generate the full changelog for the deployKF/cli repo
python ./dev/generate_changelog.py \
  --source-repo deployKF/cli \
  --output-path ./content/releases/changelogs/full-changelog-cli.md \
  --output-heading "Full changelog for CLI" \
  --include-headings "Significant Changes" "New Features" "Improvements" "Bug Fixes" "Documentation" "Miscellaneous" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?'

