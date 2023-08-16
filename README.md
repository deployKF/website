# deployKF - Website

The website for [deployKF](https://github.com/deployKF/deployKF).

## Local Development

1. create a clean miniconda environment using `conda create -n mkdocs python==3.11` (or use your preferred python environment manager)
    - we highly recommend NOT using full Anaconda and instead using [Miniforge or Mambaforge](https://github.com/conda-forge/miniforge)
    - on macOS, you may install Mambaforge by running `brew install --cask mambaforge` and then `conda init "$(basename "${SHELL}")"` to add `conda` to your shell
2. activate your conda environment using `conda activate mkdocs`
3. install the python requirements using `pip install -r ./requirements.txt -r ./requirements-dev.txt`
4. install the [MkDocs social plugin dependencies](https://squidfunk.github.io/mkdocs-material/setup/setting-up-social-cards/#dependencies) on your computer:
    - __MacOS__
       - run `brew install cairo freetype libffi libjpeg libpng zlib`
       - you may need to run `export DYLD_FALLBACK_LIBRARY_PATH="$(brew --prefix)/lib"` for cairo to work
       - you can set `DYLD_FALLBACK_LIBRARY_PATH` permanently by adding the export to your `~/.zshrc` file
    - __Ubuntu__ 
       - run `apt-get install libcairo2-dev libfreetype6-dev libffi-dev libjpeg-dev libpng-dev libz-dev`
5. serve a local version of the website using `mkdocs serve`