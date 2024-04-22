#!/usr/bin/env bash

set -euo pipefail

THIS_SCRIPT_PATH=$(cd "$(dirname "$0")" && pwd)
cd "$THIS_SCRIPT_PATH"

# generate the changelog for the deployKF/deployKF repo (excluding pre-releases)
python ./dev/generate_changelog.py \
  --source-repo 'deployKF/deployKF' \
  --output-path ./content/releases/changelog-deploykf.md \
  --output-heading 'Changelog - deployKF' \
  --output-description 'The main changelog for deployKF.' \
  --output-intro 'This changelog lists releases of __deployKF__ that are found in the [`deployKF/deployKF`](https://github.com/deployKF/deployKF/releases) repository.' \
  --output-admonition-type '!!! danger' \
  --output-admonition-title '' \
  --output-admonition-content 'Carefully review the ___"Upgrade Notes"___ and ___"Important Notes"___ before [upgrading deployKF](../guides/upgrade.md) to a new version.' \
  --output-admonition-type '!!! info' \
  --output-admonition-title 'Tool and Dependency Versions' \
  --output-admonition-content 'See the [tool versions](./tool-versions.md) and [dependency version matrix](./version-matrix.md) pages to learn more about each release.' \
  --output-admonition-type '??? question_secondary' \
  --output-admonition-title 'Can I be notified of new releases?' \
  --output-admonition-content 'Yes. Watch the [`deployKF/deployKF`](https://github.com/deployKF/deployKF) repo on GitHub.<br>At the top right, click `Watch` → `Custom` → `Releases` then confirm by selecting `Apply`.' \
  --output-admonition-type '??? question_secondary' \
  --output-admonition-title 'What about pre-releases?' \
  --output-admonition-content 'For a changelog that includes pre-releases, see the [full-changelog](./full-changelog-deploykf.md).' \
  --include-headings-h2 "Upgrade Notes" "Important Notes" "What's Changed" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --exclude-pre-releases

# generate the full changelog for the deployKF/deployKF repo
python ./dev/generate_changelog.py \
  --source-repo 'deployKF/deployKF' \
  --output-path ./content/releases/full-changelog-deploykf.md \
  --output-heading 'Changelog (all releases) - deployKF' \
  --output-description 'The full changelog for deployKF, including pre-releases.' \
  --output-intro 'This changelog lists ALL releases of __deployKF__ (including pre-releases) that are found in the [`deployKF/deployKF`](https://github.com/deployKF/deployKF/releases) repository.' \
  --output-admonition-type '!!! info' \
  --output-admonition-title 'Return to Main Changelog' \
  --output-admonition-content 'This is the _full changelog_ for deployKF.<br>Click [__HERE__](./changelog-deploykf.md) to return to the main changelog.' \
  --output-hide-sections 'navigation' \
  --include-headings-h2 "Upgrade Notes" "Important Notes" "What's Changed" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --write-version-file-path ./variables/latest_deploykf_version.txt \
  --exclude-from-search

# generate the changelog for the deployKF/cli repo (excluding pre-releases)
python ./dev/generate_changelog.py \
  --source-repo 'deployKF/cli' \
  --output-path ./content/releases/changelog-deploykf-cli.md \
  --output-heading 'Changelog - deployKF CLI' \
  --output-description 'The main changelog for the deployKF CLI.' \
  --output-intro 'This changelog lists releases of the __deployKF CLI__ that are found in the [`deployKF/cli`](https://github.com/deployKF/cli/releases) repository.' \
  --output-admonition-type '??? question_secondary' \
  --output-admonition-title 'What about pre-releases?' \
  --output-admonition-content 'For a changelog that includes pre-releases, see the [full-changelog](./full-changelog-deploykf-cli.md).' \
  --include-headings-h2 "Upgrade Notes" "Important Notes" "What's Changed" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --exclude-pre-releases

# generate the full changelog for the deployKF/cli repo
python ./dev/generate_changelog.py \
  --source-repo 'deployKF/cli' \
  --output-path ./content/releases/full-changelog-deploykf-cli.md \
  --output-heading "Changelog (all releases) - deployKF CLI" \
  --output-description 'The full changelog for the deployKF CLI, including pre-releases.' \
  --output-intro 'This changelog lists ALL releases of the __deployKF CLI__ (including pre-releases) that are found in the [`deployKF/cli`](https://github.com/deployKF/cli/releases) repository.' \
  --output-admonition-type '!!! info' \
  --output-admonition-title 'Return to Main Changelog' \
  --output-admonition-content 'This is the _full changelog_ for the deployKF CLI.<br>Click [__HERE__](./changelog-deploykf-cli.md) to return to the main changelog.' \
  --output-hide-sections 'navigation' \
  --include-headings-h2 "Upgrade Notes" "Important Notes" "What's Changed" \
  --include-tag-names 'v[0-9]+\.[0-9]+\.[0-9]+(?:-.+)?' \
  --write-version-file-path ./variables/latest_deploykf_cli_version.txt \
  --exclude-from-search
