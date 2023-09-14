# This is the script that will go on endpoints that will send out the POST api requests to log viewer.

import requests
import json
import inotify.adapters
import socket

url = 'http://192.168.1.2:8000/publish'

# response = requests.post(url, data=json.dumps(data))

# Define the path to the log file you want to watch
log_file_path = 'dummy.log'

# Create an inotify watcher
notifier = inotify.adapters.Inotify()

try:
    # Add a watch for the log file with IN_MODIFY event
    notifier.add_watch(log_file_path, mask=inotify.constants.IN_MODIFY)

    # Create a file object to keep track of the file position
    log_file = open(log_file_path, 'r')
    log_file.seek(0, 2)  # Move to the end of the file

    while True:
        for event in notifier.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event

            new_line = log_file.readline()
            while new_line:
                data = {'message': new_line.strip(), 'source': socket.gethostname()}
                requests.post(url, json=json.dumps(data))

                print(new_line.strip())
                new_line = log_file.readline()

except KeyboardInterrupt:
    pass

finally:
    # Clean up resources
    notifier.remove_watch(log_file_path)
    # notifier.cleanup()
    log_file.close()