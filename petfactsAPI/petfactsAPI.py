#!../../flask/bin/python
import os
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
import sqlite3
from flask.json import jsonify

import logging

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'petfacts_database.sqlite')
e = create_engine(SQLALCHEMY_DATABASE_URI,
                  connect_args={'detect_types': sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES},
                  native_datetime=True)

application = Flask(__name__)
api = Api(application)

class Unsubscribe(Resource):
    """Nobody really wants to unsubscribe from pet facts. 

    """

    def __init__(self):
        super(Unsubscribe, self).__init__()
    def post(self):
         return {
                    "response_type": "ephemeral",
                    'text': 'What kind of monster are you, not wanting to be subscribed to pet facts?! Shame!'
                }, 200


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
        results = self._conn.execute(sql).returns_rows
        return results

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
        query = ("select id, fact"
               " from {pet}_facts"
               " where last_shown <= datetime('now', '-{older_than}');"
               ).format(pet=pet_type, older_than=older_than)
        fact = self._conn.execute(query).fetchone()
        # Need to update last_shown to current time so we don't repeat too often
        fact_id = fact[0]
        query = ("update {pet}_facts"
               " set last_shown = datetime('now')"
               " where id = {id}"
               ).format(pet=pet_type, id=fact_id)
        self._conn.execute(query)
        return fact[1]

    def _fetch_valid_pets(self):
        """
        Queries db table containing all valid pet types.
        :return: list of pets which have corresponding pet table.
        """
        query = "select type from pet_list;"
        return [x['type'] for x in self._conn.execute(query).fetchall()]

    def _authenticate_request(self, token):
        """
        Upon receiving token, queries db and compares to known token.
        :param token:
        :return:
        """
        return True

    def post(self):
#        if not self._authenticate_request(request.values.get('token')):
#            application.logger.error("Invalid token for request.")
#            return {
#                            'response_type': 'ephemeral',
#                            'text': 'Could not authenticate request is coming from Slack.'
#                            }

        try:
            pet_type = request.values.get('text')
            if not pet_type:
                return {"successful": False, "msg": "Couldn't retrieve text from request body."}, 400
        except Exception as e:
            return {"poop":"stink str(e)"}, 400
        else:
            pet_type = self._validate_pet_type(pet_type)
            if pet_type:
                fact = self._fetch_fact(pet_type)
                return {
                    'response_type': 'in_channel',
                    'text': 'A fact about {pet}s:\n{fact}'.format(pet=pet_type, fact=fact),
                }
            else:
                pet_list = self._fetch_valid_pets()
                return {
                    "response_type": "ephemeral",
                    'text': ('Invalid pet type; must enter only one pet type at a time.'
                             ' Please try again with one of the following types: {pets}.').format(pets=' ,'.join(pet_list).rstrip(','))
                }


api.add_resource(FetchFact, '/fetchfact')
api.add_resource(Unsubscribe, '/unsubscribe')
api.init_app(application)

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8000, debug=True)
