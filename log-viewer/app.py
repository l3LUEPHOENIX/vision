from flask import Flask, render_template, request
from flask_sse import sse
import redis

app = Flask(__name__)
app.register_blueprint(sse, url_prefix='/stream')
app.config["REDIS_URL"] = "redis://192.168.1.3"
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/publish', methods=['POST'])
def publish():
    # Handle post request
    # Should be JSON that includes data source and message.
    # Use sse publish to write data to the page
    if request.get_json():
        message = request.get_json()
        sse.publish(message, type='event')
        return "SUCCESS: JSON\n"
    else:
        return "FAILED TO PUBLISH DATA\n"

@app.route('/sources', methods=['GET','POST'])
def sources():
    # Return the sources page and POST any changes.
    if request.method == 'POST':
        data = {
            'apikey' : request.form['apikey'],
            'displayname' : request.form['displayname'],
            'containerIds' : [request.form[containerId] for containerId in request.form.keys() if 'containerId' in containerId]
        }
        return f"<h1>{data}</h1>"
    else:
        return render_template('sources.html')

if __name__ == '__main__':
    # To start with gunicorn:
    # gunicorn app:app --worker-class gevent --bind 0.0.0.0:8000
    app.run(host="0.0.0.0",port=8443,ssl_context=('cert.pem', 'key.pem'))
