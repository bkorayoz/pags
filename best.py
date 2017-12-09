
import datetime
import os
import json
import re
import csv
import psycopg2 as dbapi2
from flask import redirect, Blueprint, flash
link1 = Blueprint('link2',__name__)
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

def igdb_with_id(gameid):
    ig = igdb(igdbkey)
    result = ig.games(gameid).json()
    return result[0]

def igdb_with_ids(arr):
    ig = igdb(igdbkey)
    result = ig.games({'ids': arr}).json()
    return result

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
        try:
            for g in r['genres']:
                for gn in gamegenre:
                    if g==gn['id']:
                        r['genres'][i] = gn['name']
                i += 1
        except:
            pass
        try:
            r['total_rating'] = round(r['total_rating'],2)
        except:
            pass

    return result
