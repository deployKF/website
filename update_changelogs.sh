#!/usr/bin/env bash

set -euo pipefail

THIS_SCRIPT_PATH=$(cd "$(dirname "$0")" && pwd)
cd "$THIS_SCRIPT_PATH"

# generate the changelog for the deployKF/deployKF repo (excluding pre-releases)
python ./dev/generate_changelog.py \
  --source-repo 'deployKF/deployKF' \
  --output-path ./content/releases/changelog-deploykf.md \
  --output-heading 'Changelog - deployKF' \
  --output-description 'This changelog lists releases of __deployKF__ that are found in the [`deployKF/deployKF`](https://github.com/deployKF/deployKF/releases) repository.' \
  --output-admonition-type 'info' \
  --output-admonition-title 'Pre-releases' \
  --output-admonition-content 'For a changelog that shows pre-releases, see [the full-changelog](./full-changelog-deploykf.md) page.' \
  --include-headings-h2 "Important Notes" "What's Changed" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --exclude-pre-releases

# generate the full changelog for the deployKF/deployKF repo
python ./dev/generate_changelog.py \
  --source-repo 'deployKF/deployKF' \
  --output-path ./content/releases/full-changelog-deploykf.md \
  --output-heading 'Changelog (all releases) - deployKF' \
  --output-description 'This changelog lists ALL releases of __deployKF__ (including pre-releases) that are found in the [`deployKF/deployKF`](https://github.com/deployKF/deployKF/releases) repository.' \
  --output-admonition-type 'info' \
  --output-admonition-title 'Main Changelog' \
  --output-admonition-content 'For a changelog that hides pre-releases, see [the main changelog](./changelog-deploykf.md) page.' \
  --output-hide-sections 'navigation' \
  --include-headings-h2 "Important Notes" "What's Changed" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --write-version-file-path ./variables/latest_deploykf_version.txt

# generate the changelog for the deployKF/cli repo (excluding pre-releases)
python ./dev/generate_changelog.py \
  --source-repo 'deployKF/cli' \
  --output-path ./content/releases/changelog-deploykf-cli.md \
  --output-heading 'Changelog - deployKF CLI' \
  --output-description 'This changelog lists releases of the __deployKF CLI__ that are found in the [`deployKF/cli`](https://github.com/deployKF/cli/releases) repository.' \
  --output-admonition-type 'info' \
  --output-admonition-title 'Pre-releases' \
  --output-admonition-content 'For a changelog that shows pre-releases, see [the full-changelog](./full-changelog-deploykf-cli.md) page.' \
  --include-headings-h2 "Important Notes" "What's Changed" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --exclude-pre-releases

# generate the full changelog for the deployKF/cli repo
python ./dev/generate_changelog.py \
  --source-repo 'deployKF/cli' \
  --output-path ./content/releases/full-changelog-deploykf-cli.md \
  --output-heading "Changelog (all releases) - deployKF CLI" \
  --output-description 'This changelog lists ALL releases of the __deployKF CLI__ (including pre-releases) that are found in the [`deployKF/cli`](https://github.com/deployKF/cli/releases) repository.' \
  --output-admonition-type 'info' \
  --output-admonition-title 'Main Changelog' \
  --output-admonition-content 'For a changelog that hides pre-releases, see [the main changelog](./changelog-deploykf-cli.md) page.' \
  --output-hide-sections 'navigation' \
  --include-headings-h2 "Important Notes" "What's Changed" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --write-version-file-path ./variables/latest_deploykf_cli_version.txt
