# Log Viewer Version 0.1.4
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
- Redis
- gunicorn
- gevent

### Steps
1. Clone the repo: `git clone https://github.com/l3LUEPHOENIX/log-viewer.git`
2. Start redis server and make sure app.py has the redis address.
3. From inside repo directory, run: `gunicorn --certfile cert.pem --keyfile key.pem app:app --worker-class gevent --bind 0.0.0.0:8443`
4. Test stream: `curl -H "Content-type: application/json" -d '{"message":"Hello World!","source":"edp-provision"}' -X POST https://localhost:8443/publish -k`
5. If successful, "Hello World!" should have appeared in one of the boxes.

## Option 2: Docker
Requires:
- Docker

### Steps
1. Clone the repo: `git clone https://github.com/l3LUEPHOENIX/log-viewer.git`
2. Navigate inside the repo
3. Run: `docker compose up -d`
4. Open your web browser to `https://localhost:8443`
5. If successful, data should be flowing into the source boxes.

## Troubleshoot
### Windows
#### Error: `exec ./run.sh no such file or directory`
If when trying to run `docker compose up -d`, the log-source containers fail to launch, run: `git config --global core.autocrlf false`

Then delete the repo and re-clone it. After that, try docker compose again.

## Changes
### 0.1.1
- All python packages are installed via pip from offline packages, including gunicorn and gevent.
- gunicorn is installed and uitilized.
- bloat packages removed

### 0.1.2
- log-source1 docker container for testing
- tweaks to publisher.py to be put into log-source1 container
- tweaks to event_generator.py to be put into log-source1 container
- run.sh made in order to start both publisher.py and event_generator.py in the log-source1 container

### 0.1.3
- styling

### 0.1.4
- HTTPS
- Changeable font size
- Add and remove source boxes
- Clear button added
- Styling

### Up coming:
- input validation
- authentication (ldap)
- download log
- changeable font styles
- updates to publisher.py
    - take arguements at the command line; url, path(s), and api key
- api keys
    - generate api keys
    - delete api keys
    - manage source profiles
- downloadable watcher scripts of different types: take arguments for url, log file, and api key
    - powershell
    - python
    - bash
    - a way to start and stop watcher scripts from web ui

# log-viewer container
## app.py
The main flask app. Hows all routes and configurations.

## templates/index.html
Displays default feeds.

## static/index.js
Has all logic associated with recieving and printing the data streams to the page. All functions for user inputs.

## static/style.css
Style sheet for everything.

## Certificates (*.pem)
The ones shown here were/are used for testing, but are changed out for deployment.

# Testing
## log-source1 container (for testing)
Barebones container that has a log being monitored and traffic sent to log-viewer.

## log-source2 container (for testing)
Same files as log-source1 container, except it's running python 3.6.8 instead of 3.10

### dummy.log
The log being watched and being written to by event_generator.py

### publisher.py
This script lives on the remote server and watches a specified log file. Every time new content is added, it will send a POST request to the flask app and display it on the page.

While inotify only works for linux, I plan on finding a better, more crossplatform solution.

### event_generator.py
I used this to add automatically generate log entries for testing.

To test without having to run publisher.py

`curl -k -H 'Content-type: application/json' -d '{"version":1,"authentication":{"apikey":"INSERT-API-KEY"},"content":{"message":"Hello World","containerId":"test"}}' -X POST https://localhost:8443/publish`

`python publisher.py -k "INSERT-API-KEY" -u "https://192.168.1.2:8443/publish" -f "dummy.log" -c "provision"`