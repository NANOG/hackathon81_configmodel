interface ${name}
% if descr:
    description ${descr}
% endif
% if ipv4:
    ip address ${ipv4["address"]}/${ipv4["mask"]}
% endif
% if ipv6:
    ipv6 address ${ipv6["address"]}/${ipv6["mask"]}
% endif
% if lldp:
    lldp transmit
    lldp receive
% else:
    no lldp transmit
    no lldp receive
% endif
