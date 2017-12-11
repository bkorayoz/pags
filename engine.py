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
from message import gameReqGet, getScoreCpu, getScoreGpu
from user import getspecsId

link5 = Blueprint('link5',__name__)
gamecategory = ["Main Game", "DLC/Addon", "Expansion", "Bundle","Standalone Expansion"]
gamestatus = ["Released","Alpha","Beta","Early Access","Offline","Cancelled"]
gamegenre = [{"id":2,"name":"Point-and-click"},{"id":4,"name":"Fighting"},{"id":5,"name":"Shooter"},{"id":7,"name":"Music"},{"id":8,"name":"Platform"},{"id":9,"name":"Puzzle"},{"id":10,"name":"Racing"},{"id":11,"name":"Real Time Strategy (RTS)"},{"id":12,"name":"Role-playing (RPG)"},{"id":13,"name":"Simulator"},{"id":14,"name":"Sport"},{"id":15,"name":"Strategy"},{"id":16,"name":"Turn-based strategy (TBS)"},{"id":24,"name":"Tactical"},{"id":25,"name":"Hack and slash/Beat 'em up"},{"id":26,"name":"Quiz/Trivia"},{"id":30,"name":"Pinball"},{"id":31,"name":"Adventure"},{"id":32,"name":"Indie"},{"id":33,"name":"Arcade"}]

@link5.route('/pags')
def pags():
	if getspecsId() == None:
		spek = False
	else:
		spek = True
	return render_template('recomment.html', spec = spek)

@link5.route("/engine", methods = ['POST', 'GET'])
def engine():
	engin = True
	games1 = request.form['game1']
	games2 = request.form['game2']
	games3 = request.form['game3']

	relateds = { '0':[], '1':[], '2':[] }
	relatedids = []
	arr = []
	result = []

	name = h.igdb_with_name(games1)[0]
	related = name['games']
	# for n in range(len(related)):
	# 	relateds['0'].append(h.igdb_with_id(related[n]))
	relateds['0'] = h.igdb_with_ids(related)
	relatedids = maxgame(relateds['0'])
	if relatedids[0] not in arr:
		arr.append(relatedids[0])
	if relatedids[1] not in arr:
		arr.append(relatedids[1])

	name = h.igdb_with_name(games2)[0]
	related = name['games']
	# for n in range(len(related)):
	# 	relateds['1'].append(h.igdb_with_id(related[n]))
	relateds['1'] = h.igdb_with_ids(related)
	relatedids = maxgame(relateds['1'])

	if relatedids[0] not in arr:
		arr.append(relatedids[0])
	if relatedids[1] not in arr:
		arr.append(relatedids[1])

	name = h.igdb_with_name(games3)[0]
	related = name['games']
	# for n in range(len(related)):
	# 	relateds['2'].append(h.igdb_with_id(related[n]))
	relateds['2'] = h.igdb_with_ids(related)
	relatedids = maxgame(relateds['2'])

	if relatedids[0] not in arr:
		arr.append(relatedids[0])
	if relatedids[1] not in arr:
		arr.append(relatedids[1])

	for j in range(len(arr)):
		control = False
		for i in range(3):
			for k in range(len(relateds[str(i)])):
				if relateds[str(i)][k]['id'] == arr[j]:
					if getspecsId() == None or requirementsCompare(relateds[str(i)][k]):
						result.append(relateds[str(i)][k])
						control = True
						break
			if control:
				break

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

	return render_template('recomment.html', result = result, engin = engin)

def requirementsCompare(game):
	gamereq = gameReqGet(game['name'])
	if gamereq['Minimum']['CPU']['Intel'] == 'noreq':
		return None
	usersystem = getspecsId()
	if not usersystem:
		return None
	else:
		if int(usersystem[2][:-3]) >= int(gamereq['Minimum']['RAM'][:-3]):
			if int(getScoreCpu(usersystem[0])) >= int(getScoreCpu(gamereq['Minimum']['CPU']['Intel'])) or int(getScoreCpu(usersystem[0])) >= int(getScoreCpu(gamereq['Minimum']['CPU']['AMD'])):
				if int(getScoreGpu(usersystem[1])) >= int(getScoreGpu(gamereq['Minimum']['GPU']['Nvidia'])) or int(getScoreGpu(usersystem[1])) >= int(getScoreGpu(gamereq['Minimum']['GPU']['AMD'])):
					return True
		else:
			return False


def maxgame(input):
	maxrating = 0
	maxrating2 = 0
	max_i = 0
	max2_i = 0
	for i in range(len(input)):
		try:
			if maxrating < int(input[i]['total_rating']):
				max_i = input[i]['id']
				maxrating = input[i]['total_rating']
		except:
			pass

	for i in range(len(input)):
		try:
			if maxrating2 < int(input[i]['total_rating']) and max_i != input[i]['id']:
				max2_i = input[i]['id']
				maxrating2 = input[i]['total_rating']
		except:
			pass

	ret = []
	ret.append(max_i)
	ret.append(max2_i)
	return ret
