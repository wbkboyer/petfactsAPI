#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, g
import sqlite3
import json

JSON_MIME_TYPE = 'application/json'

def json_response(data='', status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE

    return make_response(data, status, headers)


application = Flask(__name__)


@application.route('/')
def index():
    return "Welcome to the Petfacts API!"

if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0")
