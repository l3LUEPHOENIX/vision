# Log Viewer Version 1.3
View remote log contents in real time on a web page.

Remote servers have a python script watching specific log files and send POST requests every time new content is added to the log file.

# Try it!

Requires:
- Python
    - Flask
    - Flask-sse
    - inotify
    - requests
    - redis
- Redis
- gunicorn
- gevent
- Docker

1. Clone the repo:
`git clone https://github.com/l3LUEPHOENIX/log-viewer.git`

2. Navigate inside the repo

3. Run: `docker compose up -d`

4. Open your web browser to `http://localhost:8000`

5. You should see logs populating in both boxes... tada!

Lots more work to come... this is just the beginning of a greater project... hopefully.

## Troubleshoot
### Windows
#### exec ./run.sh no such file or directory
If when trying to run `docker compose up -d`, the log-source containers fail to launch, run: `git config --global core.autocrlf false`

Then delete the repo and re-clone it. After that, try docker compose again.

## Changes
### 1.1
- All python packages are installed via pip from offline packages, including gunicorn and gevent.
- gunicorn is installed and uitilized.
- bloat packages removed

### 1.2
- log-source1 docker container for testing
- tweaks to publisher.py to be put into log-source1 container
- tweaks to event_generator.py to be put into log-source1 container
- run.sh made in order to start both publisher.py and event_generator.py in the log-source1 container

### 1.3
- styling

Up coming:
- HTTPS
- string validation and termination
- authentication? (ldap)
- Download log
- changeable fonts (sizes and styles)
- api keys?
- add and remove sources
- downloadable watcher scripts of different types: take arguments for url, log file, and api key
    - powershell
    - python
    - bash
    - a way to start and stop watcher scripts from web ui

# log-viewer container
## app.py
The flask front end... Nothing too special here. Establishes routes and publishes incoming data.

## index.html
This is the only document for now. It contains all necessary styling and javascript.

# log-source1 container (for testing)
Barebones container that has a log being monitored and traffic sent to log-viewer.

# log-source2 container (for testing)
Same files as log-source1 container, except it's running python 3.6.8 instead of 3.10

## dummy.log
The log being watched and being written to by event_generator.py

## publisher.py
This script lives on the remote server and watches a specified log file. Every time new content is added, it will send a POST request to the flask app and display it on the page.

To test without having to run publisher.py
`curl -H "Content-type: application/json" -d '{"message":"Hello World!","source":"edp"}' -X POST http://localhost:8000/publish`

While inotify only works for linux, I plan on finding a better, more crossplatform solution.

## event_generator.py
I used this to add automatically generate log entries for testing.
