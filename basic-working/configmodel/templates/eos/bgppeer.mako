router bgp ${local_asn}
% if peer_v4:
    neighbor ${peer_v4} remote-as ${peer_asn}
% endif
% if peer_v6:
    neighbor ${peer_v6} remote-as ${peer_asn}
% endif
