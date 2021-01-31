"""Render configurations from schemas."""

from mako.template import Template  # type: ignore


def render(family, schema, config):
    """Return a text blob given a family, schema, and config JSON."""
    template = Template(
        filename="./configmodel/templates/{family}/{schema}.mako".format(
            family=family, schema=schema
        )
    )
    return template.render(**config)
