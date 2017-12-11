import datetime
import os
import json
import re
import psycopg2 as dbapi2
from flask import redirect, Blueprint
from flask.helpers import url_for
from flask import Flask
from flask import render_template
from flask import request
from flask_login import UserMixin, LoginManager
from passlib.apps import custom_app_context as pwd_context
from flask import current_app
dsn = """user='vagrant' password='vagrant' host='localhost' port=5432 dbname='pags'"""

class User(UserMixin):
    def __init__(self, name,email,psw):
        self.name = name
        self.email = email
        self.psw = psw

    def get_id(self):
        with dbapi2._connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT ID FROM USERDB WHERE (NAME = %s)"
            cursor.execute(query, (self.name,))
            usr = cursor.fetchone()
            return usr

    def get_user(self, id):
        with dbapi2._connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT NAME, EMAIL, PSW FROM USERDB WHERE (ID = %s)"
            cursor.execute(query, (id,))
            bla =cursor.fetchone()
            usr = User(bla[0], bla[1], bla[2])
            return usr

class UserList:
    def __init__(self):
        self.last_key = None

    def add_user(self, newuser):
        with dbapi2._connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO USERDB (NAME, EMAIL, PSW) VALUES (%s, %s, %s)"
            cursor.execute(query, (newuser.name,newuser.email, newuser.psw))
            connection.commit()
            self.last_key = cursor.lastrowid

    def verify_user(self,uname,upsw):
        with dbapi2._connect(current_app.config['dsn']) as connection:  
            cursor = connection.cursor()
            query = "SELECT NAME, PSW FROM USERDB WHERE (NAME = %s)"
            cursor.execute(query, (uname,))
            usr = cursor.fetchone()
            print (usr)
            if usr == None:
                return -2 # user yok

            else:
                if pwd_context.verify(upsw,usr[1]):
                    return 0 # sifre dogru
                else:
                    return -1 # sifre yanlis
