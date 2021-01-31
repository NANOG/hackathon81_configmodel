"""Interface Junos template tests."""

import unittest

from configmodel.templates.render import render


class TestInterface(unittest.TestCase):
    """Interface unit tests."""

    def test_pass_a(self):
        """Name only."""
        config = {"name": "et-0/0/0"}
        actual = render("junos", "interface", config)
        expected = """interfaces {
    et-0/0/0 {
        unit 0 {
        }
    }
}
"""
        assert actual == expected

    def test_pass_b(self):
        """Good ipv4 only."""
        config = {"name": "et-0/0/0", "ipv4": {"address": "192.0.2.0", "mask": 31}}
        actual = render("junos", "interface", config)
        expected = """interfaces {
    et-0/0/0 {
        unit 0 {
            family inet {
                address 192.0.2.0/31;
            }
        }
    }
}
"""
        assert actual == expected

    def test_pass_c(self):
        """Good ipv4 and ipv6."""
        config = {
            "name": "et-0/0/0",
            "ipv4": {"address": "192.0.2.0", "mask": 31},
            "ipv6": {"address": "2001:db8:c057:e110::0", "mask": 127},
        }
        actual = render("junos", "interface", config)
        expected = """interfaces {
    et-0/0/0 {
        unit 0 {
            family inet {
                address 192.0.2.0/31;
            }
            family inet6 {
                address 2001:db8:c057:e110::0/127;
            }
        }
    }
}
"""
        assert actual == expected

    # def test_fail_bad_name(self):
    #     """Invalid name."""
    #     config = {"name": "Ethernet1.1"}
    #     with open("./schemas/interface.schema.json") as f:
    #         interface_schema = json.load(f)
    #     try:
    #         validate(config, interface_schema, format_checker=FormatChecker())
    #     except ValidationError:
    #         return  # failure is success
    #     raise Exception("Should not have passed")
    #
    # def test_fail_bad_ipv4_address(self):
    #     """Invalid ipv4 address."""
    #     config = {"name": "Ethernet1", "ipv4": {"address": "192.0.2.666", "mask": 31}}
    #     with open("./schemas/interface.schema.json") as f:
    #         interface_schema = json.load(f)
    #     try:
    #         validate(config, interface_schema, format_checker=FormatChecker())
    #     except ValidationError:
    #         return  # failure is success
    #     raise Exception("Should not have passed")
    #
    # def test_fail_bad_ipv4_mask(self):
    #     """Invalid ipv4 mask."""
    #     config = {"name": "Ethernet1", "ipv4": {"address": "192.0.2.666", "mask": 33}}
    #     with open("./schemas/interface.schema.json") as f:
    #         interface_schema = json.load(f)
    #     try:
    #         validate(config, interface_schema, format_checker=FormatChecker())
    #     except ValidationError:
    #         return  # failure is success
    #     raise Exception("Should not have passed")
    #
    # def test_fail_bad_ipv6_address(self):
    #     """Invalid ipv6 address."""
    #     config = {
    #         "name": "Ethernet1",
    #         "ipv4": {"address": "192.0.2.0", "mask": 31},
    #         "ipv6": {"address": "2001:db8:FAIL:e110::0", "mask": 127},
    #     }
    #     with open("./schemas/interface.schema.json") as f:
    #         interface_schema = json.load(f)
    #     try:
    #         validate(config, interface_schema, format_checker=FormatChecker())
    #     except ValidationError:
    #         return  # failure is success
    #     raise Exception("Should not have passed")
    #
    # def test_fail_bad_ipv6_mask(self):
    #     """Invalid ipv6 mask."""
    #     config = {
    #         "name": "Ethernet1",
    #         "ipv4": {"address": "192.0.2.0", "mask": 31},
    #         "ipv6": {"address": "2001:db8:FAIL:e110::0", "mask": 666},
    #     }
    #     with open("./schemas/interface.schema.json") as f:
    #         interface_schema = json.load(f)
    #     try:
    #         validate(config, interface_schema, format_checker=FormatChecker())
    #     except ValidationError:
    #         return  # failure is success
    #     raise Exception("Should not have passed")
