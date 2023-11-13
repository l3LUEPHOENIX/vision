# Watch a directory and send all changes to Vision
import os
import requests
from inotify_simple import INotify, flags
import argparse

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

def send_post_request(event, action_type):
    file_path = os.path.join(WATCHED_DIR, event.name)
    file_name = event.name
    file_size = os.path.getsize(file_path)
    
    data = {
        'version' : 1,
        'authentication' : {
            'apikey' : args.apikey
        },
        'content' : {
            'action_type': action_type,
            'file_name' : file_name,
            'file_size' : file_size
        }
    }
    
    response = requests.post(WEB_SERVER_URL, json=data)
    if response.status_code == 200:
        print(f"File {action_type}: {file_name} ({file_size} bytes) - POST request sent")
    else:
        print(f"File {action_type}: {file_name} ({file_size} bytes) - POST request failed")

def watch_directory():
    with INotify() as ino:
        wd = ino.add_watch(WATCHED_DIR, flags.CREATE | flags.DELETE | flags.MODIFY)

        while True:
            for event in ino.read():
                for flag, _, event_name in event:
                    is_create = flag & flags.CREATE
                    is_delete = flag & flags.DELETE
                    is_modify = flag & flags.MODIFY

                    if is_create:
                        response = "created"
                    elif is_delete:
                        response = "deleted"
                    elif is_modify:
                        response = "modified"
                    send_post_request(event, response)

if __name__ == "__main__":
    print(f"Watching directory: {WATCHED_DIR}")
    watch_directory()
