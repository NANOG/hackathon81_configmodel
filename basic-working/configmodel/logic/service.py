"""Logic for service verification and translation."""

import ipaddress
import json

from jsonschema import FormatChecker, validate  # type: ignore
from sqlalchemy.orm import joinedload  # type: ignore

from configmodel.database import session
from configmodel.database.config import ConfigDB
from configmodel.database.service import ServiceDB


def validate_service(data):
    """Validate a service for a specified schema."""
    validators[data["schema"]](data["config"])


def validate_backbone_service(config):
    """Backbone schema validation."""
    # Validate device config schemas
    for configs in config.values():
        with open("./configmodel/schemas/interface.schema.json") as f:
            interface_schema = json.load(f)
        validate(configs["interface"], interface_schema, format_checker=FormatChecker())

    # Hostnames must be different
    hostnames = config.keys()
    if len(set(hostnames)) != 2:
        raise Exception("A side and Z side cannot be the same device")

    ipv4s = []
    ipv6s = []
    for configs in config.values():
        for schema, host_config in configs.items():
            if schema == "interface":  # fixme(craft): DRY
                ipv4s.append(
                    ipaddress.IPv4Interface(
                        "{}/{}".format(
                            host_config["ipv4"]["address"], host_config["ipv4"]["mask"]
                        )
                    )
                )
                ipv6s.append(
                    ipaddress.IPv6Interface(
                        "{}/{}".format(
                            host_config["ipv6"]["address"], host_config["ipv6"]["mask"]
                        )
                    )
                )

    # IP addresses must be different and in the same subnets
    validate_ips(ipv4s)
    validate_ips(ipv6s)


def validate_pni_service(config):
    """PNI schema validation."""
    # Validate device config schemas
    for configs in config.values():
        with open("./configmodel/schemas/interface.schema.json") as f:
            interface_schema = json.load(f)
        validate(configs["interface"], interface_schema, format_checker=FormatChecker())

        with open("./configmodel/schemas/bgppeer.schema.json") as f:
            bgppeer_schema = json.load(f)
        validate(configs["bgppeer"], bgppeer_schema, format_checker=FormatChecker())

    ipv4s = []
    ipv6s = []
    asns = []
    for configs in config.values():
        for schema, host_config in configs.items():
            if schema == "interface":
                ipv4s.append(
                    ipaddress.IPv4Interface(
                        "{}/{}".format(
                            host_config["ipv4"]["address"], host_config["ipv4"]["mask"]
                        )
                    )
                )
                ipv6s.append(
                    ipaddress.IPv6Interface(
                        "{}/{}".format(
                            host_config["ipv6"]["address"], host_config["ipv6"]["mask"]
                        )
                    )
                )
            if schema == "bgppeer":
                ipv4s.append(ipaddress.IPv4Interface(host_config["peer_v4"]))
                ipv6s.append(ipaddress.IPv6Interface(host_config["peer_v6"]))
                asns.append(host_config["peer_asn"])
                asns.append(host_config["local_asn"])

    # IP addresses must be different and in the same subnets
    validate_ips(ipv4s)
    validate_ips(ipv6s)

    # ASNs must be different
    validate_asns(asns, different=True)


def validate_ips(ips):
    """Validate that IPs are different and in the same subnet."""
    if len(set(ips)) == 1:
        raise Exception("A side and Z side have the same IP address (%s)" % ips[0])

    if ips[0].ip not in ips[1].network:
        raise Exception(
            "Interfaces are not in the same subnet (%s and %s)" % (ips[0], ips[1])
        )


def validate_asns(asns, different=False):
    """Validate ASNs"""
    if not different and len(asns) != 1:
        raise Exception(
            "ASNs must be the same and they are not (%s and %s)" % (asns[0], asns[1])
        )

    if different and len(asns) != 2:
        raise Exception("ASNs must be different and they are not (%s)" % asns[0])


validators = dict()
validators["backbone"] = validate_backbone_service
validators["pni"] = validate_pni_service


def commit_service_json_to_orm(data):
    """Translate REST model to ORM and commit."""
    config_dbs = []
    for hostname, configs in data["config"].items():
        for schema, host_config in configs.items():
            config_db = ConfigDB(hostname=hostname, schema=schema, config=host_config)
            config_dbs.append(config_db)
            session.add(config_db)

    session.commit()

    service_db = ServiceDB(schema=data["schema"], configs=config_dbs)
    session.add(service_db)
    session.commit()

    return service_db


def translate_service_orm_to_json(orm):
    """Translate ORM to JSON for response payload."""
    ret = {"service_id": orm.service_id, "schema": orm.schema, "config": {}}
    for config in orm.configs:
        if config.hostname not in ret["config"]:
            ret["config"][config.hostname] = {}
        ret["config"][config.hostname][config.schema] = config.config

    return ret


def get_services():
    """Get all services."""
    services = session.query(ServiceDB).options(joinedload(ServiceDB.configs)).all()
    return [translate_service_orm_to_json(service) for service in services]


def get_service(service_id):
    """Get a service."""
    service = (
        session.query(ServiceDB)
        .filter_by(service_id=service_id)
        .options(joinedload(ServiceDB.configs))
        .first()
    )
    return translate_service_orm_to_json(service)


def create_service(data):
    """Create a service."""
    return commit_service_json_to_orm(data)


def delete_service(service_id) -> bool:
    """Delete a service."""
    service = (
        session.query(ServiceDB)
        .filter_by(service_id=service_id)
        .options(joinedload(ServiceDB.configs))
        .first()
    )
    if service is None:
        return False
    session.delete(service)
    session.commit()
    return True
