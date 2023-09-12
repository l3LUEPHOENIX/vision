# Try it!
Clone the repo:
`git clone https://github.com/l3LUEPHOENIX/log-viewer.git`

Navigate inside the repo

**Obviously, you need docker and might also need to install docker compose**
Run: `docker compose up -d`

Open your web browser to `http://localhost:8000`

**curl must be installed on your system**
Open up a terminal and run: `curl -H "Content-type: application/json" -d '{"message":"Hello World!"}' -X POST http://localhost:8000/publish`

You should see "Hello World" pop up in textbox... tada!

Lots more work to come... this is just the beginning of a greater project... hopefully.

# Log Viewer Version 1.1
View remote log contents in real time on a web page.

Remote servers have a python script watching specific log files and send POST requests every time new content is added to the log file.

Dependancies:
- Flask
- Flask-sse
- inotify
- requests
- redis

## Changes
1.1:
    - All python packages are installed via pip from offline packages, including gunicorn and gevent.
    - gunicorn is installed and uitilized.
    - bloat packages removed

Up coming:
    - HTTPS
    - Form for creating more sources, and the display windows for each of those sources.
    - string validation and termination
    - authentication?
    - stylesheets

# app.py
The flask front end... Nothing too special here. Establishes routes and publishes incoming data.

# publisher.py
This script lives on the remote server and watches a specified log file. Every time new content is added, it will send a POST request to the flask app and display it on the page.

To test without having to run publisher.py
`curl -H "Content-type: application/json" -d '{"message":"Hello World!"}' -X POST http://localhost:8000/publish`

While inotify only works for linux, I plan on finding a better, more crossplatform solution.

# event_generator.py
I used this to add automatically generate log entries for testing.
