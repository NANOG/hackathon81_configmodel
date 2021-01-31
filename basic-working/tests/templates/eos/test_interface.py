"""Interface EOS template tests."""

import unittest

from configmodel.templates.render import render


class TestInterface(unittest.TestCase):
    """Interface unit tests."""

    def test_pass_a(self):
        """Name only."""
        config = {"name": "Ethernet1"}
        actual = render("eos", "interface", config)
        expected = """interface Ethernet1
    no lldp transmit
    no lldp receive
"""
        assert actual == expected

    def test_pass_b(self):
        """Good ipv4 only."""
        config = {"name": "Ethernet1", "ipv4": {"address": "192.0.2.0", "mask": 31}}
        actual = render("eos", "interface", config)
        expected = """interface Ethernet1
    ip address 192.0.2.0/31
    no lldp transmit
    no lldp receive
"""
        assert actual == expected

    def test_pass_c(self):
        """Good ipv4 and ipv6."""
        config = {
            "name": "Ethernet1",
            "ipv4": {"address": "192.0.2.0", "mask": 31},
            "ipv6": {"address": "2001:db8:c057:e110::0", "mask": 127},
        }
        actual = render("eos", "interface", config)
        expected = """interface Ethernet1
    ip address 192.0.2.0/31
    ipv6 address 2001:db8:c057:e110::0/127
    no lldp transmit
    no lldp receive
"""
        assert actual == expected

    def test_pass_d(self):
        """Good lldp enabled."""
        config = {
            "name": "Ethernet1",
            "ipv4": {"address": "192.0.2.0", "mask": 31},
            "ipv6": {"address": "2001:db8:c057:e110::0", "mask": 127},
            "lldp": True,
        }
        actual = render("eos", "interface", config)
        expected = """interface Ethernet1
    ip address 192.0.2.0/31
    ipv6 address 2001:db8:c057:e110::0/127
    lldp transmit
    lldp receive
"""
        assert actual == expected

    def test_pass_e(self):
        """Good lldp disabled."""
        config = {
            "name": "Ethernet1",
            "ipv4": {"address": "192.0.2.0", "mask": 31},
            "ipv6": {"address": "2001:db8:c057:e110::0", "mask": 127},
            "lldp": False,
        }
        actual = render("eos", "interface", config)
        expected = """interface Ethernet1
    ip address 192.0.2.0/31
    ipv6 address 2001:db8:c057:e110::0/127
    no lldp transmit
    no lldp receive
"""
        assert actual == expected
