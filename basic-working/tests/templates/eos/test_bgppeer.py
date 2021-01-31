"""BGP peer EOS template tests."""

import unittest

from configmodel.templates.render import render


class TestBGPPeer(unittest.TestCase):
    """BGP peer unit tests."""

    def test_pass_a(self):
        """Local AS only."""
        config = {"local_asn": 666}
        actual = render("eos", "bgppeer", config)
        expected = """router bgp 666
"""
        assert actual == expected

    def test_pass_b(self):
        """Good ipv4 only."""
        config = {"local_asn": "666", "peer_asn": "666", "peer_v4": "192.0.2.1"}
        actual = render("eos", "bgppeer", config)
        expected = """router bgp 666
    neighbor 192.0.2.1 remote-as 666
"""
        assert actual == expected

    def test_pass_c(self):
        """Good ipv4 and ipv6."""
        config = {
            "local_asn": "666",
            "peer_asn": "666",
            "peer_v4": "192.0.2.1",
            "peer_v6": "2001:db8:c057:e110::1",
        }
        actual = render("eos", "bgppeer", config)
        expected = """router bgp 666
    neighbor 192.0.2.1 remote-as 666
    neighbor 2001:db8:c057:e110::1 remote-as 666
"""
        assert actual == expected
