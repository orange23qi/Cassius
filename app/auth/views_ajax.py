# -*-coding: utf-8-*-
from flask import jsonify, render_template, url_for, Response, request, redirect, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from . import auth
from app.main import *


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    post_user = request.form.get('username')
    user = User.query.filter_by(username=post_user).first()

    if post_user is None:
        return redirect(url_for('main.index'))

    if user is None:
        print "ER_ROW_18"
        return jsonify(status=-1, msg='请联系管理员', data=None)

    else:
        print "SUCCESS_22"
        session['user'] = user.username
        login_user(user, True)
        print "SUCCESS_25"
        print jsonify(status=1, msg='ok', chenqi="123")
        return jsonify(status=1, msg='ok', chenqi="123")