"""Interface schema tests."""

import json
import unittest

from jsonschema import FormatChecker, validate, ValidationError  # type: ignore


class TestInterface(unittest.TestCase):
    """Interface unit tests."""

    def setUp(self) -> None:
        with open("./configmodel/schemas/interface.schema.json") as f:
            self.interface_schema = json.load(f)

    def test_pass_a(self):
        """Name only."""
        config = {"name": "Ethernet1"}
        validate(config, self.interface_schema, format_checker=FormatChecker())

    def test_pass_a_junos(self):
        """Name only."""
        config = {"name": "et-0/0/0"}
        validate(config, self.interface_schema, format_checker=FormatChecker())

    def test_pass_b(self):
        """Good ipv4 only."""
        config = {
            "name": "Ethernet1",
            "ipv4": {"address": "192.0.2.0", "mask": 31},
        }
        validate(config, self.interface_schema, format_checker=FormatChecker())

    def test_pass_c(self):
        """Good ipv4 and ipv6."""
        config = {
            "name": "Ethernet1",
            "ipv4": {"address": "192.0.2.0", "mask": 31},
            "ipv6": {"address": "2001:db8:c057:e110::0", "mask": 127},
        }
        validate(config, self.interface_schema, format_checker=FormatChecker())

    def test_fail_bad_name(self):
        """Invalid name."""
        config = {"name": "Ethernet1.1"}
        try:
            validate(config, self.interface_schema, format_checker=FormatChecker())
        except ValidationError:
            return  # failure is success
        raise Exception("Should not have passed")

    def test_fail_bad_ipv4_address(self):
        """Invalid ipv4 address."""
        config = {
            "name": "Ethernet1",
            "ipv4": {"address": "192.0.2.666", "mask": 31},
        }
        try:
            validate(config, self.interface_schema, format_checker=FormatChecker())
        except ValidationError:
            return  # failure is success
        raise Exception("Should not have passed")

    def test_fail_bad_ipv4_mask(self):
        """Invalid ipv4 mask."""
        config = {
            "name": "Ethernet1",
            "ipv4": {"address": "192.0.2.666", "mask": 33},
        }
        try:
            validate(config, self.interface_schema, format_checker=FormatChecker())
        except ValidationError:
            return  # failure is success
        raise Exception("Should not have passed")

    def test_fail_bad_ipv6_address(self):
        """Invalid ipv6 address."""
        config = {
            "name": "Ethernet1",
            "ipv4": {"address": "192.0.2.0", "mask": 31},
            "ipv6": {"address": "2001:db8:FAIL:e110::0", "mask": 127},
        }
        try:
            validate(config, self.interface_schema, format_checker=FormatChecker())
        except ValidationError:
            return  # failure is success
        raise Exception("Should not have passed")

    def test_fail_bad_ipv6_mask(self):
        """Invalid ipv6 mask."""
        config = {
            "name": "Ethernet1",
            "ipv4": {"address": "192.0.2.0", "mask": 31},
            "ipv6": {"address": "2001:db8:c057:e110::0", "mask": 666},
        }
        try:
            validate(config, self.interface_schema, format_checker=FormatChecker())
        except ValidationError:
            return  # failure is success
        raise Exception("Should not have passed")

    def test_fail_bad_lldp(self):
        """Invalid lldp."""
        config = {
            "name": "Ethernet1",
            "ipv4": {"address": "192.0.2.0", "mask": 31},
            "ipv6": {"address": "2001:db8:c057:e110::0", "mask": 127},
            "lldp": "transmit",
        }
        try:
            validate(config, self.interface_schema, format_checker=FormatChecker())
        except ValidationError:
            return  # failure is success
        raise Exception("Should not have passed")
