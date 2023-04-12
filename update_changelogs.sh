#!/usr/bin/env bash

set -euo pipefail

THIS_SCRIPT_PATH=$(cd "$(dirname "$0")" && pwd)
cd "$THIS_SCRIPT_PATH"

# generate the changelog for the deployKF/deployKF repo (excluding pre-releases)
python ./dev/generate_changelog.py \
  --source-repo deployKF/deployKF \
  --output-path ./content/releases/changelogs/changelog-deploykf.md \
  --output-heading "Changelog for deployKF" \
  --output-description 'This changelog includes all final releases of the deployKF generator source that are found in the [`deployKF/deployKF`](https://github.com/deployKF/deployKF) repository.' \
  --include-headings "Significant Changes" "New Features" "Improvements" "Bug Fixes" "Documentation" "Miscellaneous" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --exclude-pre-releases

# generate the full changelog for the deployKF/deployKF repo
python ./dev/generate_changelog.py \
  --source-repo deployKF/deployKF \
  --output-path ./content/releases/changelogs/full-changelog-deploykf.md \
  --output-heading "Full changelog for deployKF" \
  --output-description 'This changelog includes all releases (including pre-releases) of the deployKF generator source that are found in the [`deployKF/deployKF`](https://github.com/deployKF/deployKF) repository.' \
  --include-headings "Significant Changes" "New Features" "Improvements" "Bug Fixes" "Documentation" "Miscellaneous" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?'

# generate the changelog for the deployKF/cli repo (excluding pre-releases)
python ./dev/generate_changelog.py \
  --source-repo deployKF/cli \
  --output-path ./content/releases/changelogs/changelog-cli.md \
  --output-heading "Changelog for CLI" \
  --output-description 'This changelog includes all final releases of the deployKF CLI that are found in the [`deployKF/cli`](https://github.com/deployKF/cli) repository.' \
  --include-headings "Significant Changes" "New Features" "Improvements" "Bug Fixes" "Documentation" "Miscellaneous" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --exclude-pre-releases

# generate the full changelog for the deployKF/cli repo
python ./dev/generate_changelog.py \
  --source-repo deployKF/cli \
  --output-path ./content/releases/changelogs/full-changelog-cli.md \
  --output-heading "Full changelog for CLI" \
  --output-description 'This changelog includes all releases (including pre-releases) of the deployKF CLI that are found in the [`deployKF/cli`](https://github.com/deployKF/cli) repository.' \
  --include-headings "Significant Changes" "New Features" "Improvements" "Bug Fixes" "Documentation" "Miscellaneous" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?'

