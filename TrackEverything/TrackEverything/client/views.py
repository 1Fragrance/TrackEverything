from flask import render_template
from flask_login import login_required

from . import client


@client.route('/')
def index():
    return render_template('client/index.html', title="Index page")


@client.route('/dashboard')
@login_required
def dashboard():
    return render_template('сlient/dashboard.html', title="Dashboard")
