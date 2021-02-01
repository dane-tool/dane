import copy
import itertools
import json
import yaml

with open('/config.json', 'r') as infile:
    config = json.load(infile)

with open('/compose/template.yml', 'r') as infile:
    compose_template = yaml.full_load(infile)

with open('/compose/parts.yml', 'r') as infile:
    parts = yaml.full_load(infile)

# Our compose file to write
compose = copy.deepcopy(compose_template)

# Get all desired network conditions
conditions = config['conditions']

# Get all target behavior scripts to run
behaviors = config['behaviors']

# For each set of desired network conditions, we'll add a network and corres-
# ponding `router` service into the compose file.
#
# Within each set of network conditions, add `client` services for each target
# behavior, connected to the proper network.
for condition in conditions:

    latency = condition['latency']
    bandwidth = condition['bandwidth']

    # Create the network and router referencing it.
    network = copy.deepcopy(parts['network'])
    network_name = f'{latency}-{bandwidth}'
    
    compose['networks'][network_name] = network
    
    router = copy.deepcopy(parts['router'])
    router_name = f'router-{network_name}'
    router['networks'][network_name] = router['networks'].pop('NETWORK_VALUE')
    router['labels']['com.netem.tc.latency'] = latency
    router['labels']['com.netem.tc.bandwidth'] = bandwidth

    compose['services'][router_name] = router

    # Create the clients referencing each behavior. These should also reference
    # the network and router we just added.
    for behavior in behaviors:

        client = copy.deepcopy(parts['client'])
        # This doesn't handle duplicates/replicas.
        client_name = f'client-{network_name}-{behavior}'
        client['depends_on'].append(router_name)
        client['networks'].append(network_name)
        client['labels']['com.netem.behavior'] = behavior

        compose['services'][client_name] = client

with open('/compose/docker-compose.yml', 'w') as outfile:
    outfile.writelines([
        '# Built by `scripts/setup/build_compose.py` during `init` phase.\n',
        '# Please do not edit, your changes will be overwritten during the next run.\n',
        '\n'
    ])

    yaml.dump(compose, outfile)
