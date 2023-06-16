# deployKF - Website

The website for [deployKF](https://github.com/deployKF/deployKF).

## Local Development

1. create a clean miniconda environment `conda create -n mkdocs python==3.11` (or use your preferred python environment manager)
    - We highly recommend NOT using full Anaconda and instead using [Miniforge or Mambaforge](https://github.com/conda-forge/miniforge).
    - On macOS you can install Mambaforge by running: `brew install --cask mambaforge` and then `conda init "$(basename "${SHELL}")"` to add `conda` to your shell.
2. activate your conda environment: `conda activate mkdocs`
3. install the python requirements: `pip install -r ./requirements.txt -r ./requirements-dev.txt`
4. install the [MkDocs social plugin dependencies](https://squidfunk.github.io/mkdocs-material/setup/setting-up-social-cards/#dependencies) on your computer:
    - __MacOS__
       - run `brew install cairo freetype libffi libjpeg libpng zlib`
       - you may need to run `export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib` for cairo to work (make it permanent by adding to your `~/.zshrc` file)
    - __Ubuntu__ 
       - run `apt-get install libcairo2-dev libfreetype6-dev libffi-dev libjpeg-dev libpng-dev libz-dev`
5. serve a local version of the website: `mkdocs serve --watch-theme`