#!../../flask/bin/python
from flask import Flask, Blueprint
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
import sqlite3
from flask.json import jsonify
#import logging
#from logging.handlers import RotatingFileHandler


e = create_engine('sqlite:///petfacts_database.sqlite',
                  connect_args={'detect_types': sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES},
                  native_datetime=True)

application = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

parser = reqparse.RequestParser()
parser.add_argument('pet_type')


class FetchFact(Resource):
    """ Handling /fetchfact <pet_type>

        Returns response containing a fact about a given pet to
        your current slack channel.

    """

    def __init__(self):
        super(FetchFact, self).__init__()
        self._conn = e.connect()

    def _verify_table_exists(self, table_name):
        """
        Return true if table exists, false otherwise.
        :param table_name:
        :return boolean:
        """
        sql = "PRAGMA table_info({})".format(table_name)
        self._conn.execute(sql)
        return len(self._conn.fetchall())

    def _validate_pet_type(self, pet_type):
        """
        Protected method to validate whether pet type sent by user is valid,
        i.e. that there is a corresponding <pet>_facts table.
        :param pet_type:
        :return: bool
        """
        pet_type = pet_type if self._verify_table_exists(pet_type+'_facts') else None
        return pet_type

    def _fetch_fact(self, pet_type, older_than="2 days"):
        """
        Fetches a fact from the appropriate db which has not been displayed for
        :param pet_type:
        :return: str
        """
        sql = ("select id, fact"
               " from {pet}_facts"
               " where last_shown <= datetime('now', '-{older_than}');"
               ).format(pet=pet_type, older_than=older_than)
        query = self._conn.execute()
        fact = query.cursor.fetchone()

        # Need to update last_shown to current time so we don't repeat too often
        fact_id = fact[0]
        sql = ("update {pet}_facts"
               " set last_shown = datetime('now')"
               " where id = {}"
               ).format(pet=pet_type, id=fact_id)
        return fact[1]

    def _fetch_valid_pets(self):
        """
        Queries db table containing all valid pet types.
        :return: list of pets which have corresponding pet table.
        """
        sql = "select type from pet_list;"
        self._conn.execute(sql)
        return [x['type'] for x in self._conn.fetchall()]

    def _authenticate_request(self, token):
        """
        Upon receiving token, queries db and compares to known token.
        :param token:
        :return:
        """
        return True

    def post(self):
        args = parser.parse_args()
        if not self._authenticate_request(args["token"]):
#            application.logger.error("Invalid token for request.")
            return jsonify({
                            'response_type': 'ephemeral',
                            'text': 'Could not authenticate request is coming from Slack.'
                            })

        pet_type = self._validate_pet_type(args["text"])
        if pet_type:
            fact = self._fetch_fact(pet_type)
#            application.logger.info("Returning {} fact.".format(pet_type))
            return jsonify({
                'response_type': 'in_channel',
                'text': 'A fact about {pet}s:\n{fact}'.format(pet=pet_type, fact=fact),
            })
        else:
            pet_list = self._fetch_valid_pets()
#	    application.logger.error("Invalid pet type: {}".format(pet_type))
            return jsonify({
                "response_type": "ephemeral",
                'text': ('Invalid pet type; must enter only one pet type at a time.'
                         ' Please try again with one of:{pets}').format(pets='\r- '.join(pet_list))
            })


api.add_resource(FetchFact, '/fetchfact')

if __name__ == '__main__':
#    handler = TimedRotatingFileHandler('/home/ubuntu/petfacts/logs/petfacts-error.log', when='midnight', interval=1)
#    handler.setLevel(logging.DEBUG)
#    application.logger.addHandler(handler)
#    application.logger.setLevel(logging.DEBUG)
    application.run(host="0.0.0.0", port='8080')
