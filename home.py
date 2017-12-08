
import datetime
import os
import json
import re
import csv
import psycopg2 as dbapi2
from flask import redirect, Blueprint, flash
link1 = Blueprint('link1',__name__)
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
from urllib.request import Request, urlopen
import http.client
import requests
from html.parser import HTMLParser


igdbkey = "e2bc1782f5f9845a007d5a7398da2cf6"

gamecategory = ["Main Game", "DLC/Addon", "Expansion", "Bundle","Standalone Expansion"]
gamestatus = ["Released","Alpha","Beta","Early Access","Offline","Cancelled"]
gamegenre = [{"id":2,"name":"Point-and-click"},{"id":4,"name":"Fighting"},{"id":5,"name":"Shooter"},{"id":7,"name":"Music"},{"id":8,"name":"Platform"},{"id":9,"name":"Puzzle"},{"id":10,"name":"Racing"},{"id":11,"name":"Real Time Strategy (RTS)"},{"id":12,"name":"Role-playing (RPG)"},{"id":13,"name":"Simulator"},{"id":14,"name":"Sport"},{"id":15,"name":"Strategy"},{"id":16,"name":"Turn-based strategy (TBS)"},{"id":24,"name":"Tactical"},{"id":25,"name":"Hack and slash/Beat 'em up"},{"id":26,"name":"Quiz/Trivia"},{"id":30,"name":"Pinball"},{"id":31,"name":"Adventure"},{"id":32,"name":"Indie"},{"id":33,"name":"Arcade"}]
debate_games = "https://www.game-debate.com/game/api/list"

debate_ex = "https://www.game-debate.com/games/index.php?g_id=1164"

@link1.route('/')
def home_page():
    
    # print("------")
    # print(search_cpu("intel(r) core(tm) i5-3427u cpu @ 1.80ghz"))
    # print(search_cpu("intel core i5-3427u"))
    # print(search_cpu("intel celeron m processor 1.50ghz"))
    # print(search_cpu("intel core2 duo e4500"))
    # print(search_cpu("AMD Athlon 64 3000+"))
    # print(search_cpu("athlon 3000+"))
    # print(search_cpu("amd ryzen tr 1900x"))
    # print("------origins intel")
    # print(search_cpu("Intel Core i5-2400S 2.5GHz"))
    # print(search_cpu("Core i5-2400S"))
    # print("------origins amd")
    # print(search_cpu("FX-6350")) # amd
    # print(search_cpu("AMD FX-6350 Six-Core")) # amd
    # print("------")
    # print(search_cpu("amd a10-7700k apu r7 graphics"))

    print(search_gpu("1080 ti"))
    return render_template('home.html')

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def remove_html_markup(s):
    tag = False
    quote = False
    out = ""
    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out

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

def search_cpu(name):
    str = "https://www.passmark.com/search/zoomsearch.php?zoom_query=" + name + "&search.x=0&search.y=0"
    try:
        r = requests.get(str).text
    except:
        return "REQUEST ERROR"
    r = remove_html_markup(r)
    h = HTMLParser()
    r = h.unescape(r)
    index2 = r.find("- Price")
    if index2 == -1:
        index2 = len(r)

    index = r.rfind("PassMark -",0,index2)
    if index == -1:
        return "NOT FOUND"
    ret = r[index+11:index2-1]

    if len(ret) > 50:
        return name + "NOT FOUND"
    return ret

def search_gpu(name):
    index = name.find("GB")
    if index == -1:
        pass
    else:
        name = name[0:index-2]

    name = name.lower()
    name = name.replace("asus","")
    name = name.replace("nvidia","")
    name = name.replace("msi","")
    name = name.replace("gigabyte","")
    name = name.replace("pascal","")
    name = name.replace("evga","")
    name = name.replace("sapphire","")
    name = name.replace("zotac","")
    name = name.replace("amd","")
    name = name.replace("frontier edition","")
    name = name.replace("gainward","")
    name = name.replace("xfx","")
    name = name.replace("powercolor","")
    name = name.replace("intel","")
    name = name.replace("pro hd","")
    name = name.replace("graphics","")
    name = name.replace("ati","")
    name = eraseFromString(name,"(",")")
    name = name.replace("  "," ")
    str = "https://www.passmark.com/search/zoomsearch.php?zoom_query=" + name + " price performance"
    try:
        r = requests.get(str).text
    except:
        return "REQUEST ERROR"

    r = remove_html_markup(r)
    h = HTMLParser()
    r = h.unescape(r)
    index2 = r.find("- Price")
    if index2 == -1:
        index2 = len(r)

    index = r.rfind("PassMark -",0,index2)
    if index == -1:
        return "NOT FOUND"
    ret = r[index+11:index2-1]

    if len(ret) > 50:
        return name + "NOT FOUND"
    return ret

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

def checkusername(name):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ SELECT COUNT(*) FROM USERDB WHERE (NAME = %s) """
        count = cursor.execute(query,(name,))
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
            if not 6 in result[i]['platforms'] or 13 in result[i]['platforms']: # 3 linux, 6 pc-windows, 13 pc-dos, 14 mac
                del result[i]
                i -= 1
        except KeyError:
            del result[i]
            i = -1
        i+=1
    for r in result:
        r['category'] = gamecategory[r['category']]
        i = 0
        for g in r['genres']:
            for gn in gamegenre:
                if g==gn['id']:
                    r['genres'][i] = gn['name']
            i += 1
        try:
            r['rating'] = round(r['rating'],2)
        except:
            pass

    return result
