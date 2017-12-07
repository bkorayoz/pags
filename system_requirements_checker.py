import datetime
import os
import json
import csv
import re
import psycopg2 as dbapi2
from flask import redirect, Blueprint
from flask.helpers import url_for
from flask import Flask
from flask import render_template
from flask import current_app, request
from flask_login import UserMixin, LoginManager
from passlib.apps import custom_app_context as pwd_context
from flask import current_app
from home import search_cpu,search_gpu
dsn = """user='vagrant' password='vagrant' host='localhost' port=5432 dbname='pags'"""


def SystemRequirementsChecker():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        with open('CPU_UserBenchmarks.csv', newline='') as cpufile:
            cpu_index = csv.reader(cpufile, delimiter=',', quotechar='|')
            cursor = connection.cursor()
            query = """INSERT INTO CPU (NAME, SCORE, RANKING, SEARCHTERM) VALUES (%s, %s, %s, %s)"""
            for cpu in cpu_index:
                name = cpu[2] + ' ' + cpu[3]
                searcht = search_cpu(name)
                print(searcht)
                score = cpu[5]
                ranking = cpu[4]
                cursor.execute(query, (name, score, ranking,searcht))
            connection.commit()

        with open('GPU_UserBenchmarks.csv', newline='') as gpufile:
            gpu_index = csv.reader(gpufile, delimiter=',', quotechar='|')
            cursor = connection.cursor()
            query = "INSERT INTO GPU (NAME, SCORE, RANKING) VALUES (%s, %s, %s, %s)"
            for gpu in gpu_index:
                name = gpu[2] + ' ' + gpu[3]
                searcht = search_gpu(name)
                print(searcht)
                score = gpu[5]
                ranking = gpu[4]
                cursor.execute(query, (name, score, ranking, searcht))
            connection.commit()

            cursor = connection.cursor()
            ram_index = ["1 GB","2 GB","4 GB","8 GB","16 GB","32 GB","64 GB"]
            query = "INSERT INTO RAM (SIZE) VALUES (%s)"
            for ram in ram_index:
                cursor.execute(query, (ram,))
            connection.commit()
