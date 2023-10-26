from flask import Flask, render_template, request, redirect, url_for, abort, session, flash
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_sse import sse
from pydantic import ValidationError
from functools import wraps
import secrets
import os
import models

from config import *
from auth import authenticate_user

app = Flask(__name__)
app.config["SECRET_KEY"] = str(os.urandom(24).hex())
app.register_blueprint(sse, url_prefix='/stream')
app.config["REDIS_URL"] = "redis://192.168.1.3"
app.config['DEBUG'] = True
csrf = CSRFProtect(app)
MINIMUM_VERSION = 1

def vision_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('authenticated'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if authenticate_user(username, password):
            session['authenticated'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Login Failed!')
            return render_template('login.html',error=True) #flash('Login Failed!')
    else:
        return render_template('login.html',error=False)

@app.route('/')
@vision_login_required
def index():
    # Use the data stored in the database to show the index route.
    data = list(VISION_VIEWER_SOURCES.find())
    return render_template('index.html',logsources=data)

@app.route('/publish', methods=['POST'])
@csrf.exempt
def publish():
    # Handle post request
    # Should be JSON that includes data source and message.
    # Use sse publish to write data to the page
    
    if request.get_json():
        try:
            m = models.viewerApi.model_validate(request.get_json())
            sse.publish(m.post, type='event', channel=m.channel)
            del m
            return "\n\nSuccess\n\n"
        except ValidationError as e:
            return abort(400, e)
        except TypeError:
            return abort(400, m)
    else:
        return abort(400, 'POST must be JSON')


@app.route('/sources', methods=['GET','POST'])
@vision_login_required
def sources():
    # Return the sources page and POST any changes.
    if request.method == 'POST':
        apikey = {'apikey_sum': hashed_key(request.form['apikey'])}
        if request.form['actionType'] == "UPDATE":
            data = {
                "$set" : {
                    'displayname' : request.form['displayname'],
                    'containerIds' : [request.form[containerId] for containerId in request.form.keys() if 'containerId' in containerId and request.form[containerId] != '']
                }
            }
            if VISION_VIEWER_SOURCES.find_one(apikey):
                VISION_VIEWER_SOURCES.update_one(apikey,data)
            else:
                # Generate api-key and get all fields
                new_token = secrets.token_urlsafe(30)
                newdata = {
                    'apikey': encrypt(new_token, VISION_KEY),
                    'apikey_sum': hashed_key(new_token),
                    'displayname': request.form['displayname'],
                    'containerIds' : [request.form[containerId] for containerId in request.form.keys() if 'containerId' in containerId and request.form[containerId] != '']
                }
                VISION_VIEWER_SOURCES.insert_one(newdata)
            return redirect(url_for('sources'))
        elif request.form['actionType'] == "DELETE":
            VISION_VIEWER_SOURCES.delete_one(apikey)
            return redirect(url_for('sources'))
    else:
        # Turn mongo cursor object (output of find()) into a list.
        data = list(VISION_VIEWER_SOURCES.find())
        for doc in data:
            doc['apikey'] = decrypt(doc['apikey'], VISION_KEY)
        return render_template('sources.html', logsources=data)

if __name__ == '__main__':
    # To start with gunicorn:
    app.run(host="0.0.0.0",port=7443,ssl_context=('/opt/vision/secrets/cert.pem', '/opt/vision/secrets/key.pem'))
