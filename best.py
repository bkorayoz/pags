
import datetime
import os
import json
import re
import csv
import psycopg2 as dbapi2
from flask import redirect, Blueprint, flash
link2 = Blueprint('link2',__name__)
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

# route olarak link2 kullan!
igdbkey = "e2bc1782f5f9845a007d5a7398da2cf6"

gamecategory = ["Main Game", "DLC/Addon", "Expansion", "Bundle","Standalone Expansion"]
gamestatus = ["Released","Alpha","Beta","Early Access","Offline","Cancelled"]
gamegenre = [{"id":2,"name":"Point-and-click"},{"id":4,"name":"Fighting"},{"id":5,"name":"Shooter"},{"id":7,"name":"Music"},{"id":8,"name":"Platform"},{"id":9,"name":"Puzzle"},{"id":10,"name":"Racing"},{"id":11,"name":"Real Time Strategy (RTS)"},{"id":12,"name":"Role-playing (RPG)"},{"id":13,"name":"Simulator"},{"id":14,"name":"Sport"},{"id":15,"name":"Strategy"},{"id":16,"name":"Turn-based strategy (TBS)"},{"id":24,"name":"Tactical"},{"id":25,"name":"Hack and slash/Beat 'em up"},{"id":26,"name":"Quiz/Trivia"},{"id":30,"name":"Pinball"},{"id":31,"name":"Adventure"},{"id":32,"name":"Indie"},{"id":33,"name":"Arcade"}]
debate_games = "https://www.game-debate.com/game/api/list"

debate_ex = "https://www.game-debate.com/games/index.php?g_id=1164"

@link2.route("/det_search")
def det_search():
    # arr = []
    # for g in gamegenre:
    #     arr.append(g['name'])
    return render_template('detsearch.html', genres = gamegenre)

@link2.route("/send_detsearch", methods = ['GET', 'POST'])
def send_detsearch():
    if request.method == "POST":
        key = request.form['keyword']
        genre = request.form['genre']

        ig = igdb(igdbkey)
        result = ig.games({'search': key, 'filters' :{
        "[genres][eq]": genre,}}).json()
        arr = []
        for r in result:
            arr.append(r['name'])
        print(str(arr))
        return redirect(url_for('link2.det_search'))
        #return render_template('search.html',keyword = keyword, result = arr)
