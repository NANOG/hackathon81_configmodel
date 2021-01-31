autonomous-system ${local_asn};
bgp {
% if local_asn == peer_asn:
    group internal-peers {
        type internal;
% else:
    group external-peers {
        type external;
        peer-as ${peer_asn};
% endif
% if peer_v4:
        neighbor ${peer_v4};
% endif
% if peer_v6:
        neighbor ${peer_v6};
% endif
    }
}
