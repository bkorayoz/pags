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
dsn = """user='vagrant' password='vagrant' host='localhost' port=5432 dbname='pags'"""


class SystemRequirementsChecker:
    def __init__(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            with open('CPU_UserBenchmarks.csv', newline='') as cpufile:
                self.cpu_index = csv.reader(cpufile, delimiter=',', quotechar='|')
                cursor = connection.cursor()
                query = "INSERT INTO CPU (NAME, SCORE, RANKING) VALUES (%s, %s, %s)"
                for cpu in self.cpu_index:
                    name = cpu[2] + ' ' + cpu[3]
                    score = cpu[5]
                    ranking = cpu[4]
                    cursor.execute(query, (name, score, ranking))
                connection.commit()

            with open('GPU_UserBenchmarks.csv', newline='') as gpufile:
                self.gpu_index = csv.reader(gpufile, delimiter=',', quotechar='|')
                cursor = connection.cursor()
                query = "INSERT INTO GPU (NAME, SCORE, RANKING) VALUES (%s, %s, %s)"
                for gpu in self.gpu_index:
                    name = gpu[2] + ' ' + gpu[3]
                    score = gpu[5]
                    ranking = gpu[4]
                    cursor.execute(query, (name, score, ranking))
                connection.commit()

            with open('RAM_UserBenchmarks.csv', newline='') as ramfile:
                self.ram_index = csv.reader(ramfile, delimiter=',', quotechar='|')
                cursor = connection.cursor()
                query = "INSERT INTO RAM (NAME, SCORE, RANKING) VALUES (%s, %s, %s)"
                for ram in self.ram_index:
                    name = ram[2] + ' ' + ram[3]
                    score = ram[5]
                    ranking = ram[4]
                    cursor.execute(query, (name, score, ranking))
                connection.commit()
