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
# The tool utilizes an environment file (.env) located in its root directory. If
# a different location is desired, the command line option `--env`, `-e` can be
# used to specify the path of the environment file.
#
# Collected data defaults to a `data/` directory in the root of the tool. To
# output data to a different directory, the command line option `--output`, `-o`
# can be used to specify the path to the data directory.
#

import argparse
import copy
import json
import pathlib
import yaml

from pathlib import Path

def main(tool_dir, config_file, env_file, data_dir):

    print("""
Hello! Welcome to DANE.
  ____    _    _   _ _____       __/ \    
 |  _ \  / \  | \ | | ____|  ___/@    )   
 | | | |/ _ \ |  \| |  _|   O         \   
 | |_| / ___ \| |\  | |___   \_____)   \  
 |____/_/   \_\_| \_|_____|   U   \_____\ 
""")

    if config_file is None:
        config_file = str(Path(tool_dir, 'config.json'))
    
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

    # The env and data paths are used in the Compose file and are therefore
    # relative to the `built` directory in the tool. If the provided path is not
    # relative then it must be absolute.

    # We should also check that the env file exists.
    if env_file is None:
        
        path_to_check = Path(tool_dir, '.env')

        if not path_to_check.exists():
            print(f"""
Looks like your environment file doesn't exist yet. Path: {path_to_check}
We'll go ahead and create the file for you.
""")
            with open(path_to_check, 'w') as outfile:
                outfile.write("""
VPN_USERNAME=
VPN_USERGROUP=
VPN_PASSWORD=
""")
            
            if config['vpn']['enabled']:
                print(f"""
Since you have the VPN enabled, you'll need to add your login credentials now.
If you need guidance, consult https://dane-tool.github.io/dane/guide/quickstart
""")
                input(f"Please add your VPN login credentials to {path_to_check} and press Enter when you're done.")

            else:
                print(f"""
Make sure to add your login credentials to the file if you plan on using a VPN!
""")

        env_file = '../.env'
    else:
        env_file = str(Path(env_file).absolute())

    if data_dir is None:
        data_dir = '../data/'
    else:
        data_dir = str(Path(data_dir).absolute())

    
    for condition in conditions: # -- Networks, routers

        latency = condition['latency']
        bandwidth = condition['bandwidth']

        # Create the network and router referencing it.
        network = copy.deepcopy(components['network'])
        network_name = f'{latency}-{bandwidth}'
        
        compose['networks'][network_name] = network
        
        router = copy.deepcopy(components['router'])
        router_name = f'router-{network_name}'
        router['networks']['default']['aliases'].append(f'{router_name}.default')
        router['networks'][network_name] = router['networks'].pop('NETWORK_VALUE')
        router['labels']['com.dane.tc.latency'] = latency
        router['labels']['com.dane.tc.bandwidth'] = bandwidth

        compose['services'][router_name] = router

        # Create the clients referencing each behavior. These should also reference
        # the network and router we just added.
        for behavior in behaviors: # -- Clients

            client = copy.deepcopy(components['client'])
            
            # If the behavior is to use a custom script, we strip out 'custom/'
            # from the behavior to make the compose service name compatible.
            behavior_name = behavior if not behavior.startswith('custom/') else behavior[len('custom/'):]
            client_name = f'client-{network_name}-{behavior_name}'
            client['depends_on'].append(router_name)
            client['networks'].append(network_name)
            client['labels']['com.dane.behavior'] = behavior
            
            client['env_file'].append(env_file)
            client['volumes'].append(f'{data_dir}:/data/')

            # Configure whether or not the vpn will be set up, the host address,
            # etc by passing labels to each client.
            client['labels']['com.dane.vpn.enabled'] = config['vpn']['enabled']
            client['labels']['com.dane.vpn.server'] = config['vpn']['server']

            # Specify shared memory
            client['shm_size'] = config['system']['shared_memory_size']

            # NOTE: This doesn't handle duplicates/replicas. The service name
            # will be the same and thus will share the same key in the dict.
            compose['services'][client_name] = client

    # If we're configured to use local images, then remove the Docker Hub repo
    # prefix from all image entries.
    if config['system']['use_local_images']:
        print("""
Looks like you want to use local container images -- nice! Just make sure that
you've run `make build` at some point to build those local images.

If you've updated a local Dockerfile since then, run
  `make build only=<name_of_service>`
to rebuild just that image.
""")
        for service in compose['services']:
            service['image'] = service['image'].split('/')[-1]

    built_file = Path(tool_dir, 'built/docker-compose.yml')
    built_file.parent.mkdir(parents=True, exist_ok=True)
    with open(built_file, 'w') as outfile:
        outfile.writelines([
            '# Built by `build_compose.py` during `compose` phase of tool use.\n',
            '# Please do not edit, your changes will be overwritten during the next run.\n',
            '\n'
        ])

        yaml.dump(compose, outfile)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-s', '--src',
        default='.',
        help='Path to the root directory of the tool.'
    )
    parser.add_argument(
        '-c', '--config',
        default=None,
        help='File path of the desired configuration file.'
    )
    parser.add_argument(
        '-e', '--env',
        default=None,
        help='File path of the desired environment file.'
    )
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='Path to the data output directory for the tool.'
    )

    args = parser.parse_args()

    tool_dir = args.src
    config_file = args.config
    env_file = args.env
    data_dir = args.output

    main(tool_dir, config_file, env_file, data_dir)
