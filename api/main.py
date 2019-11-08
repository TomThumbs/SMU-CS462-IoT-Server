import json
# import flask
from flask import Flask, render_template
from flask_cors import CORS, cross_origin

from clients import client_api
from daily_attendance import attendance_api
from fees import fees_api
from interval import interval_api
from lastseen import lastseen_api
from missing import missing_api
from rawdata import rawdata_api
from staff import staff_api
from watchlist import watchlist_api

app = Flask(__name__)
app.config["DEBUG"] = True
# app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app)

app.register_blueprint(client_api)
app.register_blueprint(attendance_api)
app.register_blueprint(fees_api)
app.register_blueprint(interval_api)
app.register_blueprint(lastseen_api)
app.register_blueprint(missing_api)
app.register_blueprint(rawdata_api)
app.register_blueprint(staff_api)
app.register_blueprint(watchlist_api)

@app.route('/', methods=['GET'])
def home():
    # return render_template('index.html')
    return "API For IoT"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    # app.run()