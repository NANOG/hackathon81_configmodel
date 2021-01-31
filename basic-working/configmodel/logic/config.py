"""Logic for configuration verification."""

import json
import logging

from jsonschema import FormatChecker, validate  # type: ignore

from configmodel.database import session
from configmodel.database.config import ConfigDB

logging.basicConfig()
LOG = logging.getLogger(__name__)


def validate_config(data):
    """Validate a configuration for a specified schema."""
    validators[data["schema"]](data["config"])


def validate_interface_config(config):
    """Interface schema validation."""
    with open("./configmodel/schemas/interface.schema.json") as f:
        interface_schema = json.load(f)
    validate(config, interface_schema, format_checker=FormatChecker())


def validate_bgppeer_config(config):
    """BGP peer schema validation."""
    with open("./configmodel/schemas/bgppeer.schema.json") as f:
        bgppeer_schema = json.load(f)
    validate(config, bgppeer_schema, format_checker=FormatChecker())


validators = dict()
validators["interface"] = validate_interface_config
validators["bgppeer"] = validate_interface_config


def get_configs():
    """Get all configs."""
    return session.query(ConfigDB).all()


def get_config(config_id):
    """Get a config."""
    return session.query(ConfigDB).filter_by(config_id=config_id).first()


def create_config(hostname, schema, config):
    """Create a config."""
    config_db = ConfigDB(hostname=hostname, schema=schema, config=config)
    session.add(config_db)
    session.commit()
    return config_db


def delete_config(config_id) -> bool:
    """Delete a config."""
    config_db = session.query(ConfigDB).filter_by(config_id=config_id).first()
    if config_db is None:
        return False
    session.delete(config_db)
    session.commit()
    return True
