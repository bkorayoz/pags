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
from home import search_cpu, search_gpu, igdb_with_name, igdb_with_id,igdb_with_ids
from message import gameReqGet, getScoreCpu, getScoreGpu
from user import getspecsId

link5 = Blueprint('link5',__name__)

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
	bla = []

	name = igdb_with_name(games1)[0]
	related = name['games']
	# for n in range(len(related)):
	# 	relateds['0'].append(igdb_with_id(related[n]))
	relateds['0'] = igdb_with_ids(related)
	relatedids = maxgame(relateds['0'])
	if relatedids[0] not in arr:
		arr.append(relatedids[0])
	if relatedids[1] not in arr:
		arr.append(relatedids[1])

	name = igdb_with_name(games2)[0]
	related = name['games']
	# for n in range(len(related)):
	# 	relateds['1'].append(igdb_with_id(related[n]))
	relateds['1'] = igdb_with_ids(related)
	relatedids = maxgame(relateds['1'])

	if relatedids[0] not in arr:
		arr.append(relatedids[0])
	if relatedids[1] not in arr:
		arr.append(relatedids[1])

	name = igdb_with_name(games3)[0]
	related = name['games']
	# for n in range(len(related)):
	# 	relateds['2'].append(igdb_with_id(related[n]))
	relateds['2'] = igdb_with_ids(related)
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
						bla.append(relateds[str(i)][k])
						control = True
						break
			if control:
				break

	return render_template('recomment.html', result = bla, engin = engin)

def requirementsCompare(game):
	gamereq = gameReqGet(game['name'])
	usersystem = getspecsId()
	print("usersystem: " + str(usersystem))
	print("game name: " + str(game['name']))
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
	print("max game return: " + str(ret))
	return ret