"""BGP peer schema tests."""

import json
import unittest

from jsonschema import FormatChecker, validate, ValidationError  # type: ignore


class TestBGPPeer(unittest.TestCase):
    """BGP peer unit tests."""

    def setUp(self) -> None:
        with open("./configmodel/schemas/bgppeer.schema.json") as f:
            self.bgppeer_schema = json.load(f)

    def test_pass_a(self):
        """ASNs only."""
        config = {"local_asn": 666, "peer_asn": 666}
        validate(config, self.bgppeer_schema, format_checker=FormatChecker())

    def test_pass_a_32bit(self):
        """ASNs only."""
        config = {"local_asn": 4200000000, "peer_asn": 666}
        validate(config, self.bgppeer_schema, format_checker=FormatChecker())

    def test_pass_b(self):
        """Good ipv4 only."""
        config = {"local_asn": 666, "peer_asn": 666, "peer_v4": "192.0.2.0"}
        validate(config, self.bgppeer_schema, format_checker=FormatChecker())

    def test_pass_c(self):
        """Good ipv4 and ipv6."""
        config = {
            "local_asn": 666,
            "peer_asn": 666,
            "peer_v4": "192.0.2.0",
            "peer_v6": "2001:db8:c057:e110::0",
        }
        validate(config, self.bgppeer_schema, format_checker=FormatChecker())

    def test_fail_bad_local_asn(self):
        """Invalid AS."""
        config = {"local_asn": 0, "peer_asn": 666}
        try:
            validate(config, self.bgppeer_schema, format_checker=FormatChecker())
        except ValidationError:
            return  # failure is success
        raise Exception("Should not have passed")

    def test_fail_bad_peer_asn(self):
        """Invalid AS."""
        config = {"local_asn": 666, "peer_asn": -1}
        try:
            validate(config, self.bgppeer_schema, format_checker=FormatChecker())
        except ValidationError:
            return  # failure is success
        raise Exception("Should not have passed")

    def test_fail_bad_ipv4_address(self):
        """Invalid ipv4 address."""
        config = {"local_asn": 666, "peer_v4": "192.0.2.666"}
        try:
            validate(config, self.bgppeer_schema, format_checker=FormatChecker())
        except ValidationError:
            return  # failure is success
        raise Exception("Should not have passed")

    def test_fail_bad_ipv6_address(self):
        """Invalid ipv6 address."""
        config = {
            "local_asn": 666,
            "peer_asn": 666,
            "peer_v4": "192.0.2.0",
            "peer_v6": "2001:db8:fail:e110::0",
        }
        try:
            validate(config, self.bgppeer_schema, format_checker=FormatChecker())
        except ValidationError:
            return  # failure is success
        raise Exception("Should not have passed")
