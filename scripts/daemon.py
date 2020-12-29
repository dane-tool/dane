import docker
import logging
import sys

# Docker logs only show stdout of PID 1 -- so we'll write directly to that!
logger = logging.getLogger()
logger.addHandler(logging.FileHandler('/proc/1/fd/1'))
logger.setLevel(logging.INFO)

def redirect_to_out(command):
    """
    Reformats a command for docker exec so that the command output is redirected
    to the stdout of PID 1 (in order to show up in the docker log).
    """
    return f'sh -c "{command} >> /proc/1/fd/1"'

project_name = 'netem'
label_prefix = 'com.netem.'

# The DOCKER_HOST environment variable should already be defined
api = docker.from_env()

# We'll do the setup for each container as it is created. To do this, we'll
# listen for docker 'start' events, and use a callback.
def set_up_client(event):
    """
    Callback to docker startup event listener
    """

    client = api.containers.get(event['id'])
    logging.info(f"Setting up {client.name}")

    # Network emulation

    # Start by getting all traffic control labels. These are rules that we will
    # directly use to emulate conditions.
    #
    # We end up with a mapping of tc rules to their arguments.
    # e.g. {"delay": "100ms 20ms distribution normal"}
    rule_names = [label for label in client.labels if label.startswith(label_prefix+'tc')]
    rules = {
        name.split('.')[-1]: client.labels.get(name)
        for name in rule_names
    }

    # tc will take in all rules and arguments as simply space separated.
    rule_string = ' '.join([f"{k} {v}" for k,v in rules.items()])
    tc_command = f"tc qdisc add dev eth0 root netem {rule_string}"

    # Now we need to create a traffic controller container connected to this
    # container's network in order to run the command
    api.containers.run(
        image="netem-controller",
        cap_add="NET_ADMIN", network=f"container:{client.name}",
        command=tc_command,
        detach=True
    )

    logging.info(f'Network emulation for {client.name} complete.')

    # Behavior launching
    behavior = client.labels.get(label_prefix+'behavior')

    behavior_command = None
    if behavior == 'ping':
        behavior_command = 'ping -i 3 8.8.8.8'
    else:
        #! TODO: Will add browsing and streaming scripts in the future
        pass

    client.exec_run(redirect_to_out(behavior_command), detach=True)

    logging.info(f'Behavior script for {client.name} running.')

    # Network-stats collection

    #! TODO: Add data directory mount to save results; Run network-stats!
    # client.exec_run(network_stats_command, detach=True)

#! TODO: Implement timeout.
# 
# The daemon doesn't need to wait forever for setup. Also, after setup is
# complete, the containers should run for a set amount of time then be
# interrupted and cleaned up.
for event in api.events(decode=True, filters={'event': 'start'}):
    labels = event['Actor']['Attributes']
    is_netem = labels.get('com.docker.compose.project') == project_name
    is_daemon = labels.get('com.docker.compose.service') == 'daemon'
    if is_netem and not is_daemon:
        set_up_client(event)
