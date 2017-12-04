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
from flask_login import login_manager, login_user, logout_user, confirm_login,current_user
from urllib.parse import urlparse, urljoin
from classes import UserList,User
from igdb_api_python.igdb import igdb
link1 = Blueprint('link1',__name__)

igdbkey = "e2bc1782f5f9845a007d5a7398da2cf6"


gamecategory = ["Main Game", "DLC/Addon", "Expansion", "Bundle","Standalone Expansion"]
gamestatus = ["Released","Alpha","Beta","Early Access","Offline","Cancelled"]

@link1.route('/')
def home_page():
    # ig = igdb(igdbkey)
    # t = ig.platforms({'search': 'windows', 'fields': ['name']} ).text
    #res = list(t['games'])
    #res_json = json.dumps(res)
    # ig = igdb("e2bc1782f5f9845a007d5a7398da2cf6")

    # arr = range(999)
    # result = ig.games({'ids':arr}).body
    # file = open("games.txt","w")
    # file.write(str(t))
    # file.close()
    return render_template('home.html')

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@link1.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        Flag = current_app.store.verify_user(request.form['uname'], request.form['psw'])
        if Flag == 0:
            user = User(request.form['uname'],"zzz", "zzz").get_user(User(request.form['uname'],"zzz", "zzz").get_id())
            login_user(user)
            next = url_for('link3.userProfile')
            if not is_safe_url(next):
                return abort(400)
            confirm_login()
            return redirect(url_for('link3.userProfile'))
        elif Flag == -1:
            flash('Wrong Password!')
        else:
            flash('No Such User!')
        return redirect(url_for('link1.home_page'))
    else:
        flash('Unauthorized Access!')
        return redirect(url_for('link1.home_page'))

@link1.route('/signup', methods = ['GET', 'POST'])
def signup():
        return render_template('signup.html')

@link1.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You Logged Out!')
    return redirect(url_for('link1.home_page'))
#
@link1.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        userpsw0 = request.form['psw']
        userpwd1 = request.form['psw-repeat']
        if userpsw0 != userpwd1:
            flash('Passwords do not match!')
            return redirect(url_for('link1.signup'))
        else:
            userName = request.form['name']
            if checkusername(userName) == False:
                flash('Username is taken!')
                return redirect(url_for('link1.signup'))
            useremail = request.form['email']
            userpsw = pwd_context.encrypt(userpsw0)
            nuser = User(userName,useremail,userpsw)
            current_app.store.add_user(nuser)
        return redirect(url_for('link1.home_page'))
    else:
        flash("Unauthorized Access")
        return redirect(url_for('link1.home_page'))

@link1.route("/search", methods = ['GET', 'POST'])
def search():
    if request.method == "POST":
        keyword = request.form['keyword']
        arr = igdb_with_name(keyword)
        return render_template('search.html',keyword = keyword, result = arr)
    else:
        flash("Unauthorized Access")
        return redirect(url_for('link1.home_page'))

# def get_clubs():
#     with dbapi2.connect(current_app.config['dsn']) as connection:
#         cursor = connection.cursor()
#         query = """ SELECT ID, NAME, TYPE FROM CLUBDB WHERE (ACTIVE = 1) """
#         cursor.execute(query)
#         arr = cursor.fetchall()
#         return arr
#
def checkusername(name):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ SELECT COUNT(*) FROM USERDB WHERE (NAME = %s) """
        count = cursor.execute(query,(name,))
        print(count)
        if cursor.fetchone()[0] == 0:
            return True
        else:
            return False

def getuserfav(uid):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ SELECT GAMEID FROM USERFAV WHERE (USERID = %s) """
        cursor.execute(query,(uid,))
        arr = cursor.fetchall()
        return arr

def getuserrec(uid):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ SELECT GAMEID,DATE FROM USERREC WHERE (USERID = %s) """
        cursor.execute(query,(uid,))
        arr = cursor.fetchall()
        return arr

def getuserspec(uid):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ SELECT * FROM SYSDB WHERE (USERID = %s) """
        cursor.execute(query,(uid,))
        arr = cursor.fetchone()
        return arr

def igdb_with_id(gameid):
    ig = igdb(igdbkey)
    result = ig.games(gameid).json()
    return result[0]

def igdb_with_name(gamename):
    ig = igdb(igdbkey)
    #result = ig.games({'search': gamename, 'expand' : ['genres']}).json()
    result = ig.games({'search': gamename}).json()
    i = 0
    while i < len(result):
        try:
            print(result[i]['name'] + " -- " + str(result[i]['platforms']))
            if not 6 in result[i]['platforms'] or 13 in result[i]['platforms']: # 3 linux, 6 pc-windows, 13 pc-dos, 14 mac
                del result[i]
                i -= 1
        except KeyError:
            del result[i]
            i = -1
        i+=1
    for r in result:
        r['category'] = gamecategory[r['category']]
        try:
            r['rating'] = round(r['rating'],2)
        except:
            pass

    return result
