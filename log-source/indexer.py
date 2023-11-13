# Watch a directory and send all changes to Vision
import os
import requests
import inotify.adapters
import argparse
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning from urllib3 needed for self-signed certificates
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

argParser = argparse.ArgumentParser(
    prog="Vision Indexer",
    description="Watches a given directory for any changes and reports them to Vision."
)
argParser.add_argument("-d","--directory",help="The directory to watch", required=True)
argParser.add_argument("-u","--url",help="URL to Vision", required=True)
argParser.add_argument("-k","--apikey",help="Api Key to authenticate with Vision", required=True)
args = argParser.parse_args()

# Replace these with your own values
WATCHED_DIR = args.directory
WEB_SERVER_URL = args.url

def send_post_request(file_path, file_name, action_type):
    file_size = os.path.getsize(file_path)
    
    data = {
        'version' : 1,
        'authentication' : {
            'apikey' : args.apikey
        },
        'content' : {
            'action_type': str(action_type),
            'file_name' : str(file_name),
            'file_size' : str(file_size)
        }
    }
    
    response = requests.post(WEB_SERVER_URL, json=data, verify=False)
    if response.status_code == 200:
        print(f"File {action_type}: {file_name} ({file_size} bytes) - POST request sent")
    else:
        print(f"File {action_type}: {file_name} ({file_size} bytes) - POST request failed")

def watch_directory():
    notifier = inotify.adapters.Inotify()
    watch_mask = inotify.constants.IN_CREATE | inotify.constants.IN_MODIFY | inotify.constants.IN_DELETE
    notifier.add_watch(args.directory, watch_mask)

    while True:
        for event in notifier.event_gen(yield_nones=False):
            (_,type_names,path,filename) = event
            if 'IN_CREATE' in type_names:
                response = "created"
            elif 'IN_MODIFY' in type_names:
                response = "modified"
            elif 'IN_DELETE' in type_names:
                response = "deleted"

            send_post_request(path, filename, response)

if __name__ == "__main__":
    print(f"Watching directory: {WATCHED_DIR}")
    watch_directory()
