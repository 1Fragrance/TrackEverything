from flask import abort, render_template
from flask_login import current_user, login_required
from . import client


@client.route('/')
def index():
    return render_template('client/index.html', title="Index page")


@client.route('/dashboard')
@login_required
def dashboard():
    return render_template('client/dashboard.html', title="Dashboard")


