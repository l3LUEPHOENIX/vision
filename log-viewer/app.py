from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sse import sse
import pymongo
import secrets
import os
import redis
import models

app = Flask(__name__)
app.register_blueprint(sse, url_prefix='/stream')
app.config["REDIS_URL"] = "redis://192.168.1.3"
app.config['DEBUG'] = True
MINIMUM_VERSION = 1

# Create a mongodb client
client = pymongo.MongoClient(os.environ['MONGODB_HOSTNAME'], 27017, username=os.environ['MONGODB_USERNAME'],password=os.environ['MONGODB_PASSWORD'])

# Get the Log Viewer database from mongodb
db = client["log_viewer_db"]
# Get/Create the sources collection in monogdb
log_sources = db["sources"]

@app.route('/')
def index():
    # Use the data stored in the database to show the index route.
    data = list(log_sources.find())
    return render_template('index.html',logsources=data)

@app.route('/publish', methods=['POST'])
def publish():
    # Handle post request
    # Should be JSON that includes data source and message.
    # Use sse publish to write data to the page
    if request.get_json():
        incomingPost = models.publisher(request.get_json(), list(log_sources.find()))
        postValid = incomingPost.validPost(MINIMUM_VERSION)
        if postValid[0]:
            sse.publish(incomingPost.post, type='event', channel=incomingPost.channel)
            del incomingPost
            return postValid[1]
        else:
            del incomingPost
            return abort(400, postValid[1])
    else:
        return abort(400,"Data must be JSON")

@app.route('/sources', methods=['GET','POST'])
def sources():
    # Return the sources page and POST any changes.
    if request.method == 'POST':
        apikey = {'apikey':request.form['apikey']}
        if request.form['actionType'] == "UPDATE":
            data = {
                "$set" : {
                    'displayname' : request.form['displayname'],
                    'containerIds' : [request.form[containerId] for containerId in request.form.keys() if 'containerId' in containerId and request.form[containerId] != '']
                }
            }
            if log_sources.find_one(apikey):
                log_sources.update_one(apikey,data)
            else:
                # Generate api-key and get all fields
                newdata = {
                    'apikey': secrets.token_urlsafe(30),
                    'displayname': request.form['displayname'],
                    'containerIds' : [request.form[containerId] for containerId in request.form.keys() if 'containerId' in containerId and request.form[containerId] != '']
                }
                log_sources.insert_one(newdata)
            return redirect(url_for('sources'))
        elif request.form['actionType'] == "DELETE":
            if log_sources.find_one(apikey):
                log_sources.delete_one(apikey)
            return redirect(url_for('sources'))
    else:
        # Turn mongo cursor object (output of find()) into a list.
        data = list(log_sources.find())
        return render_template('sources.html', logsources=data)

if __name__ == '__main__':
    # To start with gunicorn:
    app.run(host="0.0.0.0",port=7443,ssl_context=('cert.pem', 'key.pem'))
