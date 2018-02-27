#!flask/bin/python
from flask import Flask, jsonify, abort, make_response

application = Flask(__name__)

@application.route('/')
def index():
    return "Welcome to the Petfacts API!"

if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0")
