# Vision Version 1.0.0
View remote log contents in real time on a web page.

Remote servers have a python script watching specific log files and send POST requests every time new content is added to the log file.

# Try it!

## Option 1: Manual Install
Requires:
- Python
    - Flask
    - Flask-sse
    - inotify
    - requests
    - redis
    - pyopenssl
    - pymongo
- Redis
- Mongodb
- gunicorn
- gevent

### Steps
1. Clone the repo: `git clone https://github.com/l3LUEPHOENIX/log-viewer.git`
2. Start redis server and make sure app.py has the redis address.
3. Change mongodb details in app.py
4. From inside repo directory, run: `gunicorn --certfile cert.pem --keyfile key.pem app:app --worker-class gevent --bind 0.0.0.0:7443`
5. Open a browser and navigate to `https://localhost:7443/sources` and add a source called "test" with a containerId of "test".
6. Copy the API Key.
7. In the browser, navigate to `https://localhost:7443/` and add the "test:test" source using the drop down at the top right of the page.
8. Replace `"INSERT-API-KEY"` with the API Key you copied from the Sources page and run: `curl -k -H 'Content-type: application/json' -d '{"version":1,"authentication":{"apikey":"INSERT-API-KEY"},"content":{"message":"Hello World","containerId":"test"}}' -X POST https://localhost:7443/publish`
9. If successful, "Hello World" should appear in the "test:test" box.


## Option 2: Docker
Requires:
- Docker
    - python:3.10
    - redis:alpine
    - mongo

### Steps
1. Clone the repo: `git clone https://github.com/l3LUEPHOENIX/log-viewer.git`
2. Navigate inside the repo
3. Run: `docker compose up -d`
4. Do steps 5-9 of the manual install

## Troubleshoot
### Windows
#### Error: `exec ./run.sh no such file or directory`
If when trying to run `docker compose up -d`, the log-source containers fail to launch, run: `git config --global core.autocrlf false`

Then delete the repo and re-clone it. After that, try docker compose again.

## Changes
### 1.0.0
- Vision exists!!!

### Up coming:
- input validation
- authentication (ldap)
- changeable font styles
- downloadable watcher scripts of different types: take arguments for url, log file, and api key
    - powershell
    - python
    - bash
    - a way to start and stop watcher scripts from web ui

# vision container
## app.py
The main flask app. Has all routes and configurations.

## templates/index.html
The page to watch streams. Add a source, and if data is flowing, the messages will appear in their respective boxes.

## static/index.js
Has all logic associated with recieving and printing the data streams to the page. All functions for user inputs.

## static/index.css
Style sheet for index.html.

## templates/sources.html
The page that will have a table of all sources, containerIds and API Keys

## static/sources.js
The logic for the buttons included in the sources.html file.

## static/sources.css
Stylin for the sources.html page.

## Certificates (*.pem)
The ones shown here were/are used for testing, but are changed out for deployment.

## publisher.py
This script lives on the remote server and watches a specified log file. Every time new content is added, it will send a POST request to the flask app and display it on the page, provided the correct details were supplied to the script (File, URL, ContainerID, API Key).

While inotify only works for linux, I plan on finding a better, more crossplatform solution.

Example: `python publisher.py -f "/path/to/logfile.log" -u "https://192.168.1.2:7443/publish" -c "provision" -k "INSER-API-KEY" `

# Testing
## log-source container (for testing)
Barebones container that has the event_generator script adding to a log file. The publisher.py script is started manually using the details from the Sources page in Vision.

### dummy.log
The log being watched and being written to by event_generator.py

### event_generator.py
I used this to add automatically generate log entries for testing.