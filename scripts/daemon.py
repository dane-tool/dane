import docker
import logging

# Docker logs only show stdout of PID 1 -- so we'll write directly to that!
logger = logging.basicConfig(
    filename='/proc/1/fd/1', # stdout of PID 1 -- Docker logs only show this!
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)

def redirect_to_out(command):
    """
    Reformats a command for docker exec so that the command output is redirected
    to the stdout of PID 1 (in order to show up in the docker log).
    """
    return f'sh -c "{command} >> /proc/1/fd/1"'

PROJECT_NAME = 'netem'
LABEL_PREFIX = 'com.netem.'

# The DOCKER_HOST environment variable should already be defined
API = docker.from_env()

# We'll do the setup for each container as it is created. To do this, we'll
# listen for docker 'start' events, and use a callback.
def set_up_client(event):
    """
    Callback to docker startup event listener
    """

    client = API.containers.get(event['id'])
    logging.info(f"Setting up `{client.name}`")

    ## Network emulation

    # Start by getting all traffic control labels. These are rules that we will
    # directly use to emulate conditions.
    #
    # We end up with a mapping of tc rules to their arguments.
    # e.g. {"delay": "100ms 20ms distribution normal"}
    rule_names = [label for label in client.labels if label.startswith(LABEL_PREFIX+'tc')]
    rules = {
        name.split('.')[-1]: client.labels.get(name)
        for name in rule_names
    }

    # tc will take in all rules and arguments as simply space separated.
    rule_string = ' '.join([f"{k} {v}" for k,v in rules.items()])
    tc_command = f"tc qdisc add dev eth0 root netem {rule_string}"

    # Now we need to create a traffic controller container connected to this
    # container's network in order to run the command
    API.containers.run(
        image="netem-controller",
        cap_add="NET_ADMIN", network=f"container:{client.name}",
        command=tc_command,
        detach=True
    )

    logging.info(f'Network emulation for `{client.name}` complete.')

    ## Behavior launching

    behavior = client.labels.get(LABEL_PREFIX+'behavior')

    behavior_command = None
    if behavior == 'ping':
        behavior_command = 'ping -i 3 8.8.8.8'
    elif behavior == 'script':
        behavior_command = 'python scripts/client/behavior.py'
    elif behavior == 'none':
        pass # Continue to sleep
    elif behavior is None:
        logging.warning(f'Target behavior for `{client.name}` not found; will sleep.')
        pass
    else:
        # TODO: Will add browsing and streaming scripts in the future
        logging.warning(f'Target behavior for `{client.name}` not recognized; will sleep.')
        pass

    client.exec_run(
        redirect_to_out(behavior_command),
        detach=True
    )

    logging.info(f'Behavior script for `{client.name}` running.')

    ## Network-stats collection

    # TODO: Add data directory mount to save results; Run network-stats!
    # client.exec_run(network_stats_command, detach=True)

# TODO: Implement timeout.
# 
# The daemon doesn't need to wait forever for setup. Also, after setup is
# complete, the containers should run for a set amount of time then be
# interrupted and cleaned up.
for event in API.events(
        # We're only looking at containers that were started from our docker
        # compose project.
        filters={
            'event': 'start',
            'type': 'container',
            'label': f'com.docker.compose.project={PROJECT_NAME}'
        },
        decode=True
    ):
    labels = event['Actor']['Attributes']
    is_daemon = labels.get('com.docker.compose.service') == 'daemon'
    if not is_daemon:
        set_up_client(event)
