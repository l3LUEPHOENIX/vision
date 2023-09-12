# Log Viewer Version 1.0
View remote log contents in real time on a web page.

Remote servers have a python script watching specific log files and send POST requests every time new content is added to the log file.

Dependancies:
- Flask
- Flask-sse
- inotify
- requests
- redis

# app.py
The flask front end... Nothing too special here. Establishes routes and publishes incoming data.

# publisher.py
This script lives on the remote server and watches a specified log file. Every time new content is added, it will send a POST request to the flask app and display it on the page.

To test without having to run publisher.py
`curl -H "Content-type: application/json" -d '{"message":"Hello World!"}' -X POST http://localhost:8000/publish`

While inotify only works for linux, I plan on finding a better, more crossplatform solution.

# event_generator.py
I used this to add automatically generate log entries for testing.
