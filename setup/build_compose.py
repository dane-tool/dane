# build_compose.py
# ================
#
# This script builds the Docker Compose file used to launch all containers
# needed by the tool, with proper volume mounts, environment variables, and
# labels for behaviors and network conditions as specified in the configuration.
#
# The script generally assumes that it is being run from the root directory of
# the tool, however this can be overridden by passing in a command line option
# `--src`, `-s` specifying the path to the tool directory.
#
# In the event a custom configuration file is desired, the command line option
# `--config`, `-c` can be used to specify the path of the config file.
#

import argparse
import copy
import json
import pathlib
import yaml

from pathlib import Path

def main(tool_dir, config_file=None):

    if config_file is None:
        with open(Path(tool_dir, 'config.json'), 'r') as infile:
            config = json.load(infile)
    else:
        with open(config_file, 'r') as infile:
            config = json.load(infile)

    with open(Path(tool_dir, 'docker/compose/base.yml'), 'r') as infile:
        compose_base = yaml.full_load(infile)

    with open(Path(tool_dir, 'docker/compose/components.yml'), 'r') as infile:
        components = yaml.full_load(infile)

    # Our compose file to write
    compose = copy.deepcopy(compose_base)

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
        network = copy.deepcopy(components['network'])
        network_name = f'{latency}-{bandwidth}'
        
        compose['networks'][network_name] = network
        
        router = copy.deepcopy(components['router'])
        router_name = f'router-{network_name}'
        router['networks'][network_name] = router['networks'].pop('NETWORK_VALUE')
        router['labels']['com.netem.tc.latency'] = latency
        router['labels']['com.netem.tc.bandwidth'] = bandwidth

        compose['services'][router_name] = router

        # Create the clients referencing each behavior. These should also reference
        # the network and router we just added.
        for behavior in behaviors:

            client = copy.deepcopy(components['client'])
            # This doesn't handle duplicates/replicas.
            client_name = f'client-{network_name}-{behavior}'
            client['depends_on'].append(router_name)
            client['networks'].append(network_name)
            client['labels']['com.netem.behavior'] = behavior

            compose['services'][client_name] = client

    with open(Path(tool_dir, 'built/docker-compose.yml'), 'w') as outfile:
        outfile.writelines([
            '# Built by `build_compose.py` during `init` phase.\n',
            '# Please do not edit, your changes will be overwritten during the next run.\n',
            '\n'
        ])

        yaml.dump(compose, outfile)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--src',
        help='Path to the root directory of the tool.'
    )
    parser.add_argument(
        '-c', '--config',
        help='File path of the desired configuration file.'
    )
    args = parser.parse_args()

    tool_dir = args.src or '.'
    config_file = args.config

    main(tool_dir, config_file)
