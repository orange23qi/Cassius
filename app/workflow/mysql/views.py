# -*-coding: utf-8-*-
from flask import render_template, url_for, Response, request, session
from flask_login import login_required, current_user, logout_user
from . import workflow_mysql


@workflow_mysql.route('/createdb/', methods=['GET', 'POST'])
@login_required
def CreateDB():
    logout_user()
    return render_template('mysql/CreateDb.html')


@workflow_mysql.route('/dml/', methods=['GET', 'POST'])
@login_required
def DML():
    return render_template('mysql/DML.html')


@workflow_mysql.route('/ddl/', methods=['GET', 'POST'])
@login_required
def DDL():
    return render_template('mysql/DDL.html')


@workflow_mysql.route('/orderdetail/ddl/', methods=['GET', 'POST'])
@login_required
def DetailDDL():
    return render_template('mysql/DDL.html')


@workflow_mysql.route('/orderdetail/dml/', methods=['GET', 'POST'])
@login_required
def DetailDML():
    return render_template('mysql/DML.html')