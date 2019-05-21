from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from . import auth
from .forms import LoginForm, RegistrationForm
from src.models.user import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(email=form.email.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        patronymic=form.patronymic.data,
                        username=form.username.data,
                        position=form.position.data,
                        status=1)
            user.password = form.password.data
            user.save()

            flash('You have successfully registered! You may now login.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            pass

    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            if not user.status == 2:
                login_user(user)
                flash("You're successfully logged in")
                return redirect(url_for('core.index'))
            else:
                flash('Sorry, but your account is banned')
        else:
            flash('Invalid email or password.')

    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')
    return redirect(url_for('auth.login'))
