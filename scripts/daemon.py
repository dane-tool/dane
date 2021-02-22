# Daemon
# ======
#
# The daemon is responsible for issuing commands to all other containers. As
# such, the daemon is essentially just funning a bunch of docker exec's.
#
# The daemon is created before all other containers, so it starts to listen for
# container startup events in order to set up the following clients and routers.
#
# When a router starts up, the daemon will examine its labels and exec a network
# emulation command in the router based on those labels.
#
# When a container starts up, the daemon will examine its labels and exec
# commands to establish a vpn connection, run automated browsing, and collect
# network-stats. Before network stats is run, a speedtest is conducted in the
# client container in order to produce accurate labels for the network-stats
# file name.
#
# After a little bit of time, the daemon will stop listening to docker startup
# events and start listening for an interrupt signal. When received, the daemon
# will teardown all clients and routers gracefully by interrupting all processes
# and waiting until the interrupts are complete before shutting down the
# containers. Then the daemon will exit itself.
#
# NOTE: Due to the way the self-timeout in implemented, any currently running
# functions seem to likewise get interrupted. Therefore it is advisable to set
# a very generous self-timeout in the function call within main.
#
# NOTE: Because a speedtest needs to be conducted before network-stats is run,
# behavior scripts launch quite a bit sooner than network-stats. This could mean
# some initial startup behavior when a particular script is launched (e.g. the
# loading of a webpage) will not be observed.
#
# TODO: The setup for each router and client should be non-blocking.
#

import asyncio
import docker
import json
import time
import logging
import re
import signal
import sys

# Docker logs only show stdout of PID 1 -- so we'll write directly to that!
logger = logging.basicConfig(
    filename='/proc/1/fd/1', # stdout of PID 1 -- Docker logs only show this!
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)

# Establish a global uncaught exception handler to log the exception
def log_exception(exc_type, exc_value, exc_traceback):
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = log_exception

def redirect_to_out(command):
    """
    Reformats a command for docker exec so that the command output is redirected
    to the stdout of PID 1 (in order to show up in the docker log).
    """
    return f'sh -c "{command} >> /proc/1/fd/1"'
    # return f'{command} >> /proc/1/fd/1'

PROJECT_NAME = 'netem'
LABEL_PREFIX = 'com.netem.'

# The DOCKER_HOST environment variable should already be defined
API = docker.from_env()

def setup_router(router):
    
    logging.info(f'[+] Setting up router `{router.name}`')

    ## Networking configuration

    # Re-route packets within the network.
    reroute_command = 'iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE'

    router.exec_run(
        reroute_command
    )

    logging.info(f'Packet rerouting for `{router.name}` complete.')

    ## Network emulation

    latency = router.labels.get(LABEL_PREFIX+'tc.latency')
    bandwidth = router.labels.get(LABEL_PREFIX+'tc.bandwidth')

    # Our tc commands simply inject delay. In order to get the observed ping as
    # close to the target as possible, we can first run a short ping test then
    # inject the difference.
    exitcode, output = router.exec_run(
        ['ping', '-w', '4', '-c', '4', '-q', '8.8.8.8']
    )


    curr_ping = float(output.decode().strip().split()[-2].split('/')[1])

    value, unit = re.match(r'(\d+)(\w+)', latency).groups()
    latency_to_inject = f'{round(max(0, float(value) - curr_ping))}{unit}'

    tc_command = f'tcset eth0 --delay {latency_to_inject} --rate {bandwidth} --direction incoming'
    router.exec_run(
        tc_command
    )

    logging.info(f'Network emulation for `{router.name}` complete.')

def teardown_router(router):

    logging.info(f'[-] Tearing down `{router.name}`.')
    router.stop()
    logging.info(f'`{router.name}` stopped.')

# We'll do the setup for each container as it is created. To do this, we'll
# listen for docker 'start' events, and use a callback.
def setup_client(client):
    """
    Callback to docker startup event listener. Runs, in order:
    1. Connect to router
    2. Connect to vpn
    3. Behavior launching
    4. Network-stats collection
    """

    logging.info(f"[+] Setting up client `{client.name}`")

    ## Connect to router

    # Connect to the internet *through* the router container. Note that the
    # router container should always have the hostname alias `router` on the
    # shared network, so we can just find the ip of that hostname.
    #
    # To support subshells $() we need to run this with sh -c.
    client.exec_run(
        ['sh', '-c', "ip route replace default via $(getent hosts router | cut -d ' ' -f 1)"]
    )

    logging.info(f'Client `{client.name}` connected to internal router.')

    ## Connect to vpn

    # The username, group, and password for our vpn are all loaded into the
    # client's environment variables. See `/.env`
    # We can use these variables to log into the vpn without the need for
    # interactivity!
    #
    # We don't want to continue with behavior launching and data collection
    # until we've successfully connected to the vpn, so we'll run openconnect
    # in a --background mode and we can wait for the foreground process to exit.
    #
    # If the label for the client says it's not enabled, don't run this!
    is_vpn_enabled = client.labels.get(LABEL_PREFIX+'vpn.enabled')
    # Note that labels are always treated as strings!
    if is_vpn_enabled != 'False':

        server = client.labels.get(LABEL_PREFIX+'vpn.server') or 'vpn.ucsd.edu'

        exitcode, output = client.exec_run([
            'sh', '-c',
            f'echo "$VPN_PASSWORD" \
            | openconnect --script ./vpnc-script --disable-ipv6 \
            -u "$VPN_USERNAME" --authgroup="$VPN_USERGROUP" --passwd-on-stdin \
            --non-inter --background \
            {server} \
            && exit 0'
        ])

        if exitcode != 0 :
            raise Exception(f'{client.name} did not connect to the VPN!')

        logging.info(f'Client `{client.name}` connected to VPN.')

    ## Behavior launching

    behavior = client.labels.get(LABEL_PREFIX+'behavior')

    behavior_command = None
    if behavior == 'ping':
        behavior_command = 'ping -i 3 8.8.8.8'
    elif behavior == 'script':
        behavior_command = 'python scripts/client/behavior.py'
    elif behavior == 'none':
        pass # Continue to sleep
    elif behavior == 'streaming':
        # This syntax needs to be used in order to run a single file as a
        # *module* so it can still utilize imports from its parent package.
        behavior_command = 'python -m scripts.selenium-browsing-automation.scripts.streaming.youtube_selenium.py'
    elif behavior == 'browsing':
        behavior_command = 'python scripts.selenium-browsing-automation.scripts.browsing.endless-scroll.py' 
    elif behavior is None:
        logging.warning(f'Target behavior for `{client.name}` not found; will sleep.')
        pass
    else:
        logging.warning(f'Target behavior for `{client.name}` not recognized; will sleep.')
        pass

    client.exec_run(
        redirect_to_out(behavior_command),
        detach=True
    )

    logging.info(f'Behavior script for `{client.name}` running.')

    ## Network-stats collection

    # Run a speedtest in the client in order to pass the correct network labels
    # to the network-stats filename. For now we're just interested in download
    # speed ('bandwidth') and ping ('latency')
    logging.info(f'Running speed test in `{client.name}`')
    exitcode, output = client.exec_run(
        'speedtest --json --no-upload'
    )
    if exitcode != 0:
        raise Exception(f'Speedtest failed in `{client.name}`')
    
    speedtest = json.loads(output)
    
    latency = round(speedtest['ping'])
    # Note that this outputs download speed in bit/s, so we'll convert to Mbit/s
    bandwidth = round(speedtest['download'] * 1e-6)

    details = f'{latency}ms-{bandwidth}mbit-{behavior}'

    network_stats_command = f'python scripts/client/collection.py {details}'

    client.exec_run(
        redirect_to_out(network_stats_command),
        detach=True
    )

    logging.info(f'Network stats on `{client.name}` running.')

def teardown_client(client):
    """
    To be used with callback to daemon interrupt listener. Runs, in order:
    1. Interrupt network-stats collection
    2. Interrupt behavior
    3. Stop container
    """

    logging.info(f'[-] Tearing down `{client.name}`.')

    # Interrupt all processes except for the main sleep. It is important that
    # we interrupt rather than kill, otherwise the network-stats data will not
    # be written to the file!
    #
    # We don't detach here because we want to wait for the interrupt to succeed.
    client.exec_run('pkill --signal SIGINT -f network-stats')
    logging.info('Network-stats interrupted.')
    client.exec_run('pkill -f --inverse "sleep infinity" --signal SIGINT')
    logging.info('All other tasks interrupted.')

    # After the client has been fully interrupted, it can be stopped.
    client.stop()
    logging.info(f'`{client.name}` stopped.')

# The daemon doesn't need to wait forever for setup. Also, after setup is
# complete, the containers should run for a set amount of time then be
# interrupted and cleaned up.
def listen_for_container_startup(timeout=15):
    """

    Returns a list of clients that have been set up.
    """

    # Register the alarm signal to send a timeout error
    def alarm_handler(signum, frame):
        raise TimeoutError('Stop listening for events!')
    signal.signal(signal.SIGALRM, alarm_handler)
    # Raise the timeout error after n seconds
    signal.alarm(timeout)

    logging.info(f'Listening for docker startup events. Will stop listening after {timeout} seconds.')

    routers = []
    clients = []

    # Listen to docker events and handle client container setup when they start.
    # If we see a TimeoutError though, then we'll halt and return.
    #
    # /\/\/\/\/\
    # TODO: To avoid race conditions where a container is able to start up
    # before this listener is started, we should first check the existing
    # containers.
    #
    # Everything should be non-blocking.
    # \/\/\/\/\/
    try:
        for event in API.events(
                # We're only looking at containers that were started from our
                # docker compose project.
                filters={
                    'event': 'start',
                    'type': 'container',
                    'label': f'com.docker.compose.project={PROJECT_NAME}'
                },
                decode=True
            ):
            labels = event['Actor']['Attributes']

            container_type = labels.get('com.netem.type')

            if container_type == 'router':
                router = API.containers.get(event['id'])
                routers.append(router)
                setup_router(router)
            elif container_type == 'client':
                client = API.containers.get(event['id'])
                clients.append(client)
                setup_client(client)
            elif container_type == 'daemon':
                pass
            else:
                logging.warning(f'Unknown container type `{container_type}` seen for {labels.get("com.docker.compose.service")}. Ignoring.')

    except TimeoutError:
        logging.info('Timeout seen.')

    logging.info('No longer listening for docker events.')
    return routers, clients

def handle_interrupt(routers, clients):

    logging.info('Daemon interrupted!')

    for client in clients:
        teardown_client(client)

    logging.info('All clients stopped.')

    for router in routers:
        teardown_router(router)

    logging.info('All container stopped, Daemon will now exit.')
    logging.info('Check `/data` for the network-stats output. Thanks for using this tool!')
    exit(0)

def listen_for_interrupt(handler, timeout=None):
    """

    Parameters
    ----------
    handler : function
        Expects a function with no arguments.
    timeout : seconds, optional
        If present, will automatically trigger interrupt after this amount of
        time.
    """

    logging.info('Listening for daemon interrupt.')
    logging.warning('\n\
========\n\
Please run `make stop` or `docker kill -s SIGINT netem_daemon_1` to stop\n\
this tool. Failure to do so will result in data loss.\n\
========')

    # TODO: If a timeout has been specified, halt after that amount of time

    # If an Interrupt has been seen, run teardown for all of the clients.
    signal.signal(signal.SIGINT, lambda signum, frame: handler())

if __name__ == "__main__":

    # Timeout needs to be sufficiently large to allow for all containers to be
    # connected to VPN, sequentially.
    #
    # TODO: Make event listener for startup non-blocking.
    routers, clients = listen_for_container_startup(timeout=200)

    listen_for_interrupt(handler=lambda: handle_interrupt(routers, clients))
    
    # While we're waiting for some signal the daemon can just chill out!
    signal.pause()
