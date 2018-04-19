from flask import render_template
from flask_login import login_required, logout_user
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    logout_user()
    return render_template('Login.html')

@main.route('/logout', methods=['GET', 'POST'])
@login_required
def Logout():
    return render_template('Login.html')