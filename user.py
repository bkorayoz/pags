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
from classes import User
from passlib.apps import custom_app_context as pwd_context
from flask_login.utils import login_required
from flask_login import login_manager, login_user, logout_user,current_user

link3 = Blueprint('link3',__name__)

@link3.route('/profile')
@login_required
def userProfile():
    uid = User(current_user.name,"zzz", "zzz").get_id()[0]
    specs = getspecs()
    return render_template('profile.html', uid = uid, specs = specs)

@link3.route('/confighw')
@login_required
def confighw():
    uid = User(current_user.name,"zzz", "zzz").get_id()[0]
    cpu = getcpu()
    gpu = getgpu()
    ram = getram()
    return render_template('confighw.html', uid = uid, cpu = cpu, gpu = gpu, ram = ram)

@link3.route('/savehw',methods=['GET', 'POST'])
@login_required
def savehw():
    if request.method == "POST":
        uid = User(current_user.name,"zzz", "zzz").get_id()[0]
        c = request.form['cpu']
        g = request.form['gpu']
        r = request.form['ram']
        o = request.form['os']
        with dbapi2._connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """ SELECT ID FROM CPU WHERE (NAME = %s) """
            cursor.execute(query,(c,))
            cid = cursor.fetchone()[0]

            query = """ SELECT ID FROM GPU WHERE (NAME = %s) """
            cursor.execute(query,(g,))
            gid = cursor.fetchone()[0]

            query = """ SELECT ID FROM RAM WHERE (SIZE = %s) """
            cursor.execute(query,(r,))
            rid = cursor.fetchone()[0]

            query = """ SELECT COUNT(*) FROM SYSDB WHERE USERID = %s """
            cursor.execute(query,(uid,))
            count = cursor.fetchone()[0]
            if count == 0:
                query = """ INSERT INTO SYSDB(USERID,GPUID,CPUID,RAMID,OSNAME) VALUES (%s, %s, %s, %s, %s) """
                cursor.execute(query,(uid,gid,cid,rid,o,))
            else:
                query = """UPDATE SYSDB SET GPUID=%s,CPUID=%s,RAMID=%s,OSNAME=%s WHERE(USERID=%s)"""
                cursor.execute(query,(gid,cid,rid,o,uid,))

        return redirect(url_for('link3.userProfile'))


def getspecs():
    uid = User(current_user.name,"zzz", "zzz").get_id()[0]
    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ SELECT CPU.NAME,GPU.NAME,RAM.SIZE FROM SYSDB,GPU,CPU,RAM
        WHERE (SYSDB.GPUID = GPU.ID AND SYSDB.CPUID = CPU.ID AND SYSDB.RAMID = RAM.ID AND SYSDB.USERID = %s)"""
        cursor.execute(query,(uid,))
        arr = cursor.fetchone()
        return arr

def getcpu():
    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ SELECT NAME,ID FROM CPU ORDER BY NAME """
        cursor.execute(query)
        arr = cursor.fetchall()
        return arr

def getgpu():
    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ SELECT NAME,ID FROM GPU ORDER BY NAME"""
        cursor.execute(query)
        arr = cursor.fetchall()
        return arr

def getram():
    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ SELECT SIZE,ID FROM RAM"""
        cursor.execute(query)
        arr = cursor.fetchall()
        return arr


@link3.route('/edit')
@login_required
def editProfile():
    return render_template('edit.html')


@link3.route('/edit_profile',methods=['GET', 'POST'])
@login_required
def updateProfile():
    if request.method == "POST":
        userpsw0 = request.form['psw']
        userpwd1 = request.form['psw-repeat']
        useremail = request.form['email']
        if userpsw0 != None:
            if userpsw0 != userpwd1:
                flash('Passwords do not match!')
                return redirect(url_for('link3.editProfile'))
            else:
                userpsw = pwd_context.encrypt(userpsw0)
                userid=current_user.get_id()
                with dbapi2._connect(current_app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = """UPDATE USERDB SET PSW=%s WHERE(ID=%s)"""
                    cursor.execute(query,(userpsw,userid,))
        if useremail!= None:
            userid=current_user.get_id()
            with dbapi2._connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """UPDATE USERDB SET EMAIL=%s WHERE(ID=%s)"""
                cursor.execute(query,(useremail,userid,))
        else:
            return redirect(url_for('link3.userProfile'))
    return redirect(url_for('link3.userProfile'))
