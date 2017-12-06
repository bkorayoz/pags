import datetime
import os
import json
import re
import psycopg2 as dbapi2
from flask import redirect, Blueprint, flash
from flask.helpers import url_for
from flask import Flask
from flask import render_template, Response
from flask import request, current_app
from passlib.apps import custom_app_context as pwd_context
from flask_login.utils import login_required
from flask_login import login_manager, login_user, logout_user,current_user

link4 = Blueprint('link4',__name__)

@link4.route('/message')
def message():
	return render_template('message.html')

@link4.route('/hwGathered/')
def hwGathered():
    uid = User(current_user.name,"zzz", "zzz").get_id()[0]
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = "SELECT GPUID, CPUID, RAMID, OSNAME FROM SYSDB WHERE (USERID = %s)"
        cursor.execute(query,(uid,))
        specs = cursor.fetchone()[0]
    return render_template('hwGathered.html', specs = specs)

@link4.route('/sysinfoget', methods = ['POST', 'GET'])
def sysinfoget():
    info = request.json
    uid = User(info['user'],"zzz", "zzz").get_id()[0]
    gpuid = info['gpu']
    cpuid = info['cpu']
    ramid = info['ram']
    osname = info['ostype']
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = "INSERT INTO SYSDB (USERID, GPUID, CPUID, RAMID, OSNAME) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query,(uid, gpuid, cpuid, ramid,ostype))
    return 

#def eraseParantez(input):