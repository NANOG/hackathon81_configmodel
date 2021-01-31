"""BGP peer Junos template tests."""

import unittest

from configmodel.templates.render import render


class TestBGPPeer(unittest.TestCase):
    """BGP peer unit tests."""

    def test_pass_a_internal(self):
        """Internal AS only."""
        config = {"local_asn": 666, "peer_asn": 666}
        actual = render("junos", "bgppeer", config)
        expected = """autonomous-system 666;
bgp {
    group internal-peers {
        type internal;
    }
}
"""
        assert actual == expected

    def test_pass_a_external(self):
        """External AS only."""
        config = {"local_asn": 666, "peer_asn": 1337}
        actual = render("junos", "bgppeer", config)
        expected = """autonomous-system 666;
bgp {
    group external-peers {
        type external;
        peer-as 1337;
    }
}
"""
        assert actual == expected

    def test_pass_b_internal_v4(self):
        """Internal and ipv4."""
        config = {"local_asn": 666, "peer_asn": 666, "peer_v4": "192.0.2.1"}
        actual = render("junos", "bgppeer", config)
        expected = """autonomous-system 666;
bgp {
    group internal-peers {
        type internal;
        neighbor 192.0.2.1;
    }
}
"""
        assert actual == expected

    def test_pass_c_internal_v4_v6(self):
        """Internal and ipv4 and ipv6."""
        config = {
            "local_asn": 666,
            "peer_asn": 666,
            "peer_v4": "192.0.2.1",
            "peer_v6": "2001:db8:c057:e110::1",
        }
        actual = render("junos", "bgppeer", config)
        expected = """autonomous-system 666;
bgp {
    group internal-peers {
        type internal;
        neighbor 192.0.2.1;
        neighbor 2001:db8:c057:e110::1;
    }
}
"""
        assert actual == expected

    def test_pass_d_external_v4_v6(self):
        """External and ipv4 and ipv6."""
        config = {
            "local_asn": 666,
            "peer_asn": 1337,
            "peer_v4": "192.0.2.1",
            "peer_v6": "2001:db8:c057:e110::1",
        }
        actual = render("junos", "bgppeer", config)
        expected = """autonomous-system 666;
bgp {
    group external-peers {
        type external;
        peer-as 1337;
        neighbor 192.0.2.1;
        neighbor 2001:db8:c057:e110::1;
    }
}
"""
        assert actual == expected
