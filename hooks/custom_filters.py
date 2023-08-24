import json
from typing import Optional

import markdown
from jinja2 import Environment
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import _RelativePathTreeprocessor


def _custom_to_json(value: str):
    return json.dumps(value)


def _md_to_html(
    value: str,
    file: File,
    files: Files,
    config: MkDocsConfig,
):
    md = markdown.Markdown(extensions=["extra", "sane_lists"])

    # for relative-path conversion, we use the upstream mkdocs implementation:
    #  - this converts paths like "./docs/foo.md" to "../docs/foo/" (relative to the current page)
    #  - https://github.com/mkdocs/mkdocs/blob/1.5.2/mkdocs/structure/pages.py#L276
    relative_path_ext = _RelativePathTreeprocessor(
        file=file, files=files, config=config
    )
    md.treeprocessors.register(relative_path_ext, "relative_path", 0)

    # convert markdown to html
    html = md.convert(value)

    # now we can replace the relative paths with absolute paths
    #  - this converts paths like "../docs/foo/" to "https://deplokf.org/docs/foo/"
    html = html.replace('href="../', f'href="{config["site_url"].rstrip("/")}/')

    return html


def on_env(
    env: Environment, config: MkDocsConfig, files: Files, **kwargs
) -> Optional[Environment]:
    # we define a wrapper here to access `config` and `files`
    def md_to_html(value: str, file: File):
        return _md_to_html(value, file, files, config)

    env.filters["custom_to_json"] = _custom_to_json
    env.filters["md_to_html"] = md_to_html
    return env
