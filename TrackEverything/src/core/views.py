from . import core
from flask import render_template
from flask_login import current_user, login_required


def is_admin():
    if not current_user.is_admin:
        return False
    return True


@core.route('/')
@login_required
def index():
    return render_template('core/index.html', title="Index page")
