from . import admin
from flask import abort, render_template
from flask_login import current_user, login_required


@admin.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('admin/dashboard.html', title="Dashboard")
