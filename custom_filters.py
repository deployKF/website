import json

import markdown
from jinja2 import Environment


def _custom_to_json(value):
    return json.dumps(value)


def _md_to_html(value):
    return markdown.markdown(value, extensions=["extra", "sane_lists"])


def on_env(env: Environment, **kwargs):
    env.filters["custom_to_json"] = _custom_to_json
    env.filters["md_to_html"] = _md_to_html
    return env
