#!../../flask/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime
import sqlite3
import argparse

def create_connection(db_file):
    """ create a database connection to the SQLite database
    specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.text_factory = str
        return conn
    except Error as e:
        print(e)
        return None


def verify_table_exists(conn, table_name):
    """
    Return true if table exists, false otherwise.
    :param conn:
    :param table_name:
    :return boolean:
    """
    sql = "PRAGMA table_info({})".format(table_name)
    cur = conn.cursor()
    cur.execute(sql)
    return len(cur.fetchall())


def add_fact(conn, pet_type, fact):
    """
    Add a new fact into the specified pet table
    :param conn:
    :param pet_type:
    :param fact:
    :return: fact id
    """
    if verify_table_exists(conn, pet_type+"_facts"):
        not_yet_shown = datetime.strptime("1970/01/01", "%Y/%m/%d")

        sql = ''' INSERT INTO {}_facts(fact, last_shown)
                  VALUES(?,?) '''.format(pet_type)
        cur = conn.cursor()
        cur.execute(sql, (fact, not_yet_shown,))
    else:
        raise ValueError("Bad table name. Aborting.")


def main(pet_type):
    # create a database connection
    with create_connection("./petfacts_database.sqlite") as conn:
        with open("./{}_facts.txt".format(pet_type), "r") as f_in:
            facts = f_in.readlines()
            for fact in facts:
                try:
                    add_fact(conn, pet_type, fact)
                except ValueError as e:
                    print(e)
                    break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--type", default="cat", help="Type of valid pet to which your facts all pertain.")

    args = parser.parse_args()

    main(args.type)
