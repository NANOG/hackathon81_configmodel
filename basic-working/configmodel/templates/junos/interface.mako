interfaces {
    ${name} {
% if descr:
        description ${descr};
% endif
        unit 0 {
% if ipv4:
            family inet {
                address ${ipv4["address"]}/${ipv4["mask"]};
            }
% endif
% if ipv6:
            family inet6 {
                address ${ipv6["address"]}/${ipv6["mask"]};
            }
% endif
        }
    }
}
