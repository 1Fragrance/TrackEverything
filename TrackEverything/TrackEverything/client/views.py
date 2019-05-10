from flask import abort, render_template
from flask_login import current_user, login_required
from . import client


def is_admin():
    if not current_user.is_admin:
        return False
    return True


@client.route('/')
@login_required
def index():
    if is_admin():
        return render_template('admin/index.html', title="Index page")
    return render_template('client/index.html', title="Index page")


