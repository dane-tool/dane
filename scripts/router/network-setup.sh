#!/bin/sh
set -e # (exit on error)

# Network Setup
# =============
#
# Expects inputs $1, $2, $3 to be the router service name, and the latency and
# bandwidth values to pass into tc, respectively.
# 
service_name="$1"
latency="$2"
bandwidth="$3"

# We configured our router on the default bridge network to have an alias of its
# service name followed by ".default". We can get the ip that alias corresponds
# to.
router_ip_ext=$(getent hosts "$service_name".default | cut -d ' ' -f1)

# Now we can find out which interface is connected to the default bridge by
# getting the interface which is home to the router ip on the default network.
iface_ext=$(ip route | grep "$router_ip_ext" | cut -d ' ' -f3)
# The interface connected to the intranet is just the opposite (replace 0 with 1
# and vice-versa)
iface_int=$(echo "$iface_ext" | tr 01 10)

# Ensure the default route for the router goes through the gateway on the
# default bridge network (external).
#
# NOTE: The gateway IP should end in .1 (from experience). This should be tested
# on other systems to ensure this assumption is valid.
gateway_ip_ext=$(echo "$router_ip_ext" | awk -F '.' '{print $1"."$2"."$3".1"}')
ip route replace default via "$gateway_ip_ext" dev "$iface_ext"

# Now we allow the router to route traffic!
#
# Truthfully I don't fully understand the workings of this command, I found it
# by talking to a networking domain expert. Will update this comment if I look
# into it further.
iptables -t nat -A POSTROUTING -o "$iface_ext" -j MASQUERADE

# Finally, we can use tc to inject latency into the external interface and set
# bandwidth on the internal interface.

# If we attempt to set latency on the internal interface, we'd end up with
# double latency since packets would be delayed being sent to and coming from
# the intranet.
#
# We can run a quick ping test to only inject the difference between our current
# and target latency (with a minimum of zero if our current latency is greater
# than the configured latency)
curr_latency=$(ping -c4 -w4 8.8.8.8 | tail -1 | cut -d'=' -f2 | cut -d'/' -f2) # Avg
tmp=$(echo "$latency" | sed -r 's/^(\d+)(\w+)$/\1 \2/')
latency_val=$(echo "$tmp" | cut -d' ' -f1)
latency_unit=$(echo "$tmp" | cut -d' ' -f2)
to_inject=$(printf %.0f $(echo "$latency_val - $curr_latency" | bc))
to_inject=$([ $to_inject -ge "0" ] && echo "$to_inject" || echo "0")
achieved_latency=$(printf %.0f $(echo "$curr_latency + $to_inject" | bc))
tc qdisc add dev "$iface_ext" root netem delay "$to_inject$latency_unit"

# We can't actually limit ingress bandwidth (that would entail preventing other
# parties from sending you data!), and utilizing an IFB interface to emulate
# ingress rate limiting doesn't work on Mac or Windows.
#
# The router approach we're using works really well for this, however, since we
# can **just limit the egress on our internal interface**! This allows our
# router to act as the buffer :)
tc qdisc add dev "$iface_int" root netem rate "$bandwidth"

exit 0
