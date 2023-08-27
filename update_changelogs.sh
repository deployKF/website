#!/usr/bin/env bash

set -euo pipefail

THIS_SCRIPT_PATH=$(cd "$(dirname "$0")" && pwd)
cd "$THIS_SCRIPT_PATH"

# generate the changelog for the deployKF/deployKF repo (excluding pre-releases)
python ./dev/generate_changelog.py \
  --source-repo 'deployKF/deployKF' \
  --output-path ./content/releases/changelog-deploykf.md \
  --output-heading 'Changelog for deployKF' \
  --output-description 'This changelog lists releases of deployKF that are found in the [`deployKF/deployKF`](https://github.com/deployKF/deployKF/releases) repository.' \
  --output-tip 'For a changelog that shows pre-releases, see [this page](../full-changelog-deploykf).' \
  --include-headings 'Significant Changes' 'New Features' 'Improvements' 'Bug Fixes' 'Documentation' 'Miscellaneous' \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --exclude-pre-releases

# generate the full changelog for the deployKF/deployKF repo
python ./dev/generate_changelog.py \
  --source-repo 'deployKF/deployKF' \
  --output-path ./content/releases/full-changelog-deploykf.md \
  --output-heading 'FULL Changelog for deployKF' \
  --output-description 'This changelog lists ALL releases of deployKF (including pre-releases) that are found in the [`deployKF/deployKF`](https://github.com/deployKF/deployKF/releases) repository.' \
  --output-tip 'For a changelog that hides pre-releases, see [this page](../changelog-deploykf).' \
  --output-hide-sections 'navigation' \
  --include-headings 'Significant Changes' 'New Features' 'Improvements' 'Bug Fixes' 'Documentation' 'Miscellaneous' \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --write-version-file-path ./variables/latest_deploykf_version.txt

# generate the changelog for the deployKF/cli repo (excluding pre-releases)
python ./dev/generate_changelog.py \
  --source-repo 'deployKF/cli' \
  --output-path ./content/releases/changelog-deploykf-cli.md \
  --output-heading 'Changelog for deployKF CLI' \
  --output-description 'This changelog lists releases of the deployKF CLI that are found in the [`deployKF/cli`](https://github.com/deployKF/cli/releases) repository.' \
  --output-tip 'For a changelog that shows pre-releases, see [this page](../full-changelog-deploykf-cli).' \
  --include-headings 'Significant Changes' 'New Features' 'Improvements' 'Bug Fixes' 'Documentation' 'Miscellaneous' \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --exclude-pre-releases

# generate the full changelog for the deployKF/cli repo
python ./dev/generate_changelog.py \
  --source-repo 'deployKF/cli' \
  --output-path ./content/releases/full-changelog-deploykf-cli.md \
  --output-heading "FULL Changelog for deployKF CLI" \
  --output-description 'This changelog lists ALL releases of the deployKF CLI (including pre-releases) that are found in the [`deployKF/cli`](https://github.com/deployKF/cli/releases) repository.' \
  --output-tip 'For a changelog that hides pre-releases, see [this page](../changelog-deploykf-cli).' \
  --output-hide-sections 'navigation' \
  --include-headings 'Significant Changes' 'New Features' 'Improvements' 'Bug Fixes' 'Documentation' 'Miscellaneous' \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --write-version-file-path ./variables/latest_deploykf_cli_version.txt

