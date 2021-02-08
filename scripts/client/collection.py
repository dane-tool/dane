# Run network-stats and save the data
import datetime
import os
import pathlib
from pathlib import Path
import sys

timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')

# For now, the naming details are passed in by the daemon.
details = sys.argv[1]
filename = f"{timestamp}_{details}.csv"

datadir = "/data/"

# For now, just call network-stats and send the output to the data mount.
os.system(f'scripts/network-stats/network_stats.py -i eth0 -e {Path(datadir, filename)}')
