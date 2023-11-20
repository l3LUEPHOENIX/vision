# This is the script that will go on endpoints that will send out the POST api requests to Vision.

import requests
import inotify.adapters
import argparse

argParser = argparse.ArgumentParser(
    prog="Vision Publisher",
    description="Watches a given file for new entries and posts them to Vision.",
)
argParser.add_argument("-f", "--file", help="Path to watched file", required=True)
argParser.add_argument("-u", "--url", help="Vision URL", required=True)
argParser.add_argument(
    "-c",
    "--containerid",
    help="The ID of the container the publsiher will post to",
    required=True,
)
argParser.add_argument("-k", "--apikey", help="API Key", required=True)

args = argParser.parse_args()

# Create an inotify watcher
notifier = inotify.adapters.Inotify()

try:
    # Add a watch for the log file with IN_MODIFY event
    notifier.add_watch(args.file, mask=inotify.constants.IN_MODIFY)

    # Create a file object to keep track of the file position
    log_file = open(args.file, "r")
    log_file.seek(0, 2)  # Move to the end of the file

    while True:
        for event in notifier.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event

            new_line = log_file.readline()
            while new_line:
                data = {
                    "version": 1,
                    "authentication": {"apikey": args.apikey},
                    "content": {
                        "message": new_line.strip(),
                        "containerId": args.containerid,
                    },
                }

                print(requests.post(args.url, json=data, verify=False).text)
                new_line = log_file.readline()

except KeyboardInterrupt:
    pass

finally:
    # Clean up resources
    notifier.remove_watch(args.file)
    # notifier.cleanup()
    log_file.close()
