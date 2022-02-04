import os

from flask import Flask, render_template
from flask.json import JSONEncoder
from flask_cors import CORS

from bson import json_util, ObjectId
from datetime import datetime


class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


def create_app():
    app_dir = os.path.abspath(os.path.dirname(__file__))
    static_folder = os.path.join(app_dir, 'templates/static')
    template_folder = os.path.join(app_dir, 'templates')

    app = Flask(__name__, static_folder=static_folder,
                template_folder=template_folder,
                )
    CORS(app)
    app.json_encoder = MongoJsonEncoder

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        return render_template('index.html')

    return app
