import datetime
import os
import json
import re
import psycopg2 as dbapi2
from home import link1

from flask import redirect
from flask.helpers import url_for
from flask import Flask, flash
from flask import render_template
from flask_login import login_manager, current_user
from flask_login.login_manager import LoginManager
from passlib.apps import custom_app_context as pwd_context
from datetime import timedelta
from flask_login.utils import login_required

app = Flask(__name__)
app.register_blueprint(link1)
app.secret_key = 'gallifrey'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'link1.home_page'
login_manager.fresh_view = 'link1.home_page'

# @login_manager.user_loader
# def load_user(user_id):
#     return User("zzz","zzz", 9999, "zzz", "zzz").get_user(user_id)
#
# @login_manager.unauthorized_handler
# def unauthorized():
#     # do stuff
#     flash("Unauthorized Access. Please Sign In or Sign Up!")
#     return redirect(url_for('link1.home_page'))
#
# def get_elephantsql_dsn(vcap_services):
#     """Returns the data source name for ElephantSQL."""
#     parsed = json.loads(vcap_services)
#     uri = parsed["elephantsql"][0]["credentials"]["uri"]
#     match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
#     user, password, host, _, port, dbname = match.groups()
#     dsn = """user='{}' password='{}' host='{}' port={}
#              dbname='{}'""".format(user, password, host, port, dbname)
#     return dsn
#

# def initdbVerification(key,kay):
#     if (ord(app.secret_key[0]) - kay) == key:
#         initialize_database()
#     return redirect(url_for('link1.home_page'))

@app.route('/initdb')
def initialize_database():
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DROP TABLE IF EXISTS USERDB CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE USERDB (ID SERIAL PRIMARY KEY,
            NAME VARCHAR(40) NOT NULL,
            EMAIL VARCHAR(50), PSW VARCHAR(200)) """
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS GPU CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE GPU (ID SERIAL PRIMARY KEY,
            NAME VARCHAR(40) NOT NULL,
            SCORE FLOAT, RANKING INT """
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS CPU CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE CPU (ID SERIAL PRIMARY KEY,
            NAME VARCHAR(40) NOT NULL,
            SCORE FLOAT, RANKING INT """
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS RAM CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE RAM (ID SERIAL PRIMARY KEY,
            NAME VARCHAR(40) NOT NULL,
            SCORE FLOAT, RANKING INT """
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS SYSDB CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE SYSDB (ID SERIAL PRIMARY KEY, USERID INT REFERENCES USERDB(ID), GPUID INT REFERENCES GPU(ID)
            CPUID INT REFERENCES CPU(ID), RAMID INT REFERENCES RAM(ID), OSNAME VARCHAR(30)"""

            query = """DROP TABLE IF EXISTS USERFAV CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE USERREC (ID SERIAL PRIMARY KEY,
            USERID INT REFERENCES USERDB(ID),GAMEID INT,DATE TIMESTAMP NOT NULL"""
            cursor.execute(query)

            query = """CREATE TABLE USERFAV (ID SERIAL PRIMARY KEY,
            USERID INT REFERENCES USERDB(ID),GAMEID INT"""
            cursor.execute(query)

            # query = """INSERT INTO USERDB(NAME,PSW,EMAIL) VALUES(%s, %s, %s)   """
            # cursor.execute(query,('koray', pwd_context.encrypt('123'), 'koray@itu.edu.tr',))
            #
            # query = """INSERT INTO USERDB(NAME,REALNAME,PSW,NUMBER,EMAIL) VALUES(%s, %s, %s, %s, %s)   """
            # cursor.execute(query,('turgut','Turgut Can Aydinalev', pwd_context.encrypt('123'),12345, 'turgut@itu.edu.tr',))
            #
            # query = """INSERT INTO USERDB(NAME,REALNAME,PSW,NUMBER,EMAIL) VALUES(%s, %s, %s, %s, %s)   """
            # cursor.execute(query,('beste','Beste Burcu Bayhan', pwd_context.encrypt('123'),12345, 'beste@itu.edu.tr',))

        flash("Database initialized.")

        return redirect(url_for('link1.home_page'))


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='pags'"""

    REMEMBER_COOKIE_DURATION = timedelta(seconds = 10)
    #app.store = UserList(os.path.join(os.path.dirname(__file__),app.config['dsn']))
    app.run(host='0.0.0.0', port=port, debug=debug)
