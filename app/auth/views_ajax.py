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
        return jsonify(status=-1, msg='请联系管理员', data=None)
        #return redirect(url_for('main.index'))

    if user is None:
        return jsonify(status=-1, msg='请联系管理员', data=None)

    else:
        session['user'] = user.username
        login_user(user, True)

        return jsonify(status=1, msg='ok')