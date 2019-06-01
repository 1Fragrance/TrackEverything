from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from src.common.messages import (ACCOUNT_BANNED_MESSAGE, LOGIN_FAILURE_MESSAGE,
                                 LOGIN_SUCCESS_MESSAGE, LOGOUT_MESSAGE,
                                 REGISTER_SUCCESS_MESSAGE)
from src.models.user import User

from . import auth
from .forms import LoginForm, RegistrationForm


"""

User register endpoint
"""
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    patronymic=form.patronymic.data,
                    username=form.username.data,
                    position=form.position.data,
                    status=1)
        user.password = form.password.data
        user.save()

        flash(REGISTER_SUCCESS_MESSAGE)
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Register')


"""

User login endpoint
"""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            if not user.status == 2:
                login_user(user)
                flash(LOGIN_SUCCESS_MESSAGE)
                return redirect(url_for('core.index'))
            else:
                flash(ACCOUNT_BANNED_MESSAGE)
        else:
            flash(LOGIN_FAILURE_MESSAGE)

    return render_template('auth/login.html', form=form, title='Login')


"""

User logout endpoint
"""
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(LOGOUT_MESSAGE)
    return redirect(url_for('auth.login'))
