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
from home import search_cpu

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

@link4.route('/gameReqGet/<gameName>')
def gameReqGet(gameName):
    print(gameName)
    rawRequirements = fetch_requirements(gameName)
    requirements = {'Minimum': {
                                 'CPU': {
                                          'Intel': hwNametoId(search_hw(eraseFromString(rawRequirements['Minimum']['CPU']['Intel'], '(', ')'))),
                                          'AMD': hwNametoId(search_hw(eraseFromString(rawRequirements['Minimum']['CPU']['AMD'], '(', ')')))
                                        },
                                 'GPU': {
                                          'Nvidia': '0',
                                          'AMD': '0'
                                        },
                                 'RAM': 0
                               },
                    # 'Recommended': {
                    #                  'CPU': {
                    #                           'Intel': hwNametoId(search_hw(eraseFromString(rawRequirements['Minimum']['CPU']['Intel'], '(', ')')), 'CPU'),
                    #                           'AMD': hwNametoId(search_hw(eraseFromString(rawRequirements['Minimum']['CPU']['AMD'], '(', ')')), 'CPU')
                    #                         },
                    #                  'GPU': {
                    #                           'Nvidia': '0',
                    #                           'AMD': '0'
                    #                         },
                    #                  'RAM': '0'
                    #                }
                   }
    print(str(requirements))
    return

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

def hwNametoId(name):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT ID FROM CPU WHERE (SEARCHTERM = %s)"""
        cursor.execute(query, (name,))
        hw_id = cursor.fetchone()[0]
    if hw_id:
        return hw_id
    else:
        return '0'
#def eraseParantez(input):
