# -*-coding: utf-8-*-
from flask import render_template, url_for, Response, request, session
from flask_login import login_required, current_user, logout_user
from . import workflow


@workflow.route('/userindex/', methods=['GET', 'POST'])
@login_required
def UserIndex():
    return render_template('UserIndex.html')