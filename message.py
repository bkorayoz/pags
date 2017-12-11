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
from fetch_game_requirements import fetch_requirements
import home as h

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
        cursor.execute(query,(uid, gpuid, cpuid, ramid, ostype))
    return

@link4.route('/gameReqGet/<gameName>')
def gameReqGet(gameName):
    rawRequirements = fetch_requirements(gameName)
    if not rawRequirements:
        return False
    requirements = {'Minimum': {
                                 'CPU': {
                                          'Intel': hwNametoIdCpu(h.search_cpu(addZero(eraseFromString(rawRequirements['Minimum']['CPU']['Intel'], '(', ')')))),
                                          'AMD': hwNametoIdCpu(h.search_cpu(addZero(eraseFromString(rawRequirements['Minimum']['CPU']['AMD'], '(', ')'))))
                                        },
                                 'GPU': {
                                          'Nvidia': hwNametoIdGpu(h.search_gpu(eraseFromString(rawRequirements['Minimum']['GPU']['Nvidia'], '(', ')'))),
                                          'AMD': hwNametoIdGpu(h.search_gpu(eraseFromString(rawRequirements['Minimum']['GPU']['AMD'], '(', ')')))
                                        },
                                 'RAM': rawRequirements['Minimum']['RAM']
                               },
                   }

    print(str(requirements))
    return requirements

def eraseFromString(term, deliminator1, deliminator2):
    tag = False
    out = ""
    for c in term:
            if c == deliminator1:
                tag = True
            elif c == deliminator2:
                tag = False
            elif not tag:
                out = out + c
    return out


def addZero(term):
    term = term.lower()
    out = ""
    index1 = term.find("ghz")
    if index1 == -1:
        return term
    index2 = term.find(".", index1-4, index1)
    if (index1 - index2) < 3:
        out = term[0: index2 + 2]
        out = out + "0" + term[index1 :]
    else:
        out = term
    return out

def hwNametoIdCpu(name):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT ID FROM CPU WHERE (SEARCHTERM = %s)"""
        cursor.execute(query, (name,))
        hw_id = cursor.fetchone()
    if hw_id:
        return hw_id[0]
    else:
        return '0'

def hwNametoIdGpu(name):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT ID FROM GPU WHERE (SEARCHTERM = %s)"""
        cursor.execute(query, (name,))
        hw_id = cursor.fetchone()
    if hw_id:
        return hw_id[0]
    else:
        return '0'

def getScoreCpu(id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT SCORE FROM CPU WHERE (ID = %s)"""
        cursor.execute(query, (id,))
        score = cursor.fetchone()
    if score:
        return score[0]
    else:
        return '0'

def getScoreGpu(id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT SCORE FROM GPU WHERE (ID = %s)"""
        cursor.execute(query, (id,))
        score = cursor.fetchone()
    if score:
        return score[0]
    else:
        return '0'

