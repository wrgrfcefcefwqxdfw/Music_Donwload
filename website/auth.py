from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
# models.py have usermixin to use current_user to access info about the current logged in user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('_flashes', None)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # filter user using email
        user = User.query.filter_by(email=email).first()
        # check if user exists
        if user:
            print('Logged in')
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                # remember if user is logged in
                #  after you restart the flask web server, this will no longer be true
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                error = 'Incorrect password or email, try again'
                return render_template("login.html", error_message=error)
        else:
            error = "Incorrect password or email, try again"
            return render_template("login.html", error_message=error)
    return render_template("login.html", user=current_user)


@auth.route('/logout')
# below decorator is so u cannot logout unless you are logged in
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    session.pop('_flashes', None)
    if request.method == 'POST':
        # request.form is in a form of a dict
        # .get to get a specific attribute
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # flash allows you to display some messages
        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists', category='error')
        elif len(email) < 4:
            flash('Email must be more than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First Name must be more than 1 character.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        elif password1 != password2:
            flash('Password do not match!', category='error')
        else:
            # add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # after sign up, log in user
            login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)
