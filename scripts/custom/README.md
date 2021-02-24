# Custom scripts for client containers

Welcome! You have the ability to add arbitrary custom Python scripts to this folder so that they can be run as the behavior of client containers.

Common scripts utilize Selenium and perform different internet browsing related activities, such as watching videos, surfing the web, downloading files, etc.

For your sanity, you should test that the script can be run within a client container successfully. Remember that a browser running in these containers *will be headless*! Add any necessary pip libraries to a `requirements.txt` file within this folder.

Remember to set the behavior string to `"custom/<filename.py>"` in the config file.
