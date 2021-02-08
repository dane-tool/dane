# Run network-stats and save the data
import datetime
import os
import pathlib
from pathlib import Path

# TODO: Eventually add naming convention for network conditions and behavior...
# or maybe just embed metadata as frontmatter, like a csvy file.

# This is just to find the container ID for the filename.
container_id = (
    os.popen("cat /proc/self/cgroup | head -1 | tr '/' '\n' | tail -1")
    .read()
    .strip()
)
timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
filename = f"{timestamp}_{container_id}.csv"

datadir = "/data/"

# For now, just call network-stats and send the output to the data mount.
os.system(f'scripts/network-stats/network_stats.py -i eth0 -e {Path(datadir, filename)}')
