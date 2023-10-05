# Import necessary Flask modules and packages
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Import the 'db' object from the '__init__.py' file
from flask_login import login_user, login_required, logout_user, current_user

# Create a Blueprint named 'auth'
auth = Blueprint('auth', __name__)

# Route for handling login (GET and POST methods)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Query the database for a user with the provided email
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('f1.optimize_f1'))  # Redirect to a specific page upon successful login
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

# Route for handling user logout
@auth.route('/logout')
@login_required  # Requires the user to be logged in to access this route
def logout():
    logout_user()
    return redirect(url_for('auth.login'))  # Redirect to the login page after logout

# Route for user registration (GET and POST methods)
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if the provided email already exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Create a new user and store it in the database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)  # Log in the new user
            flash('Account created!', category='success')
            return redirect(url_for('f1.optimize_f1'))  # Redirect to a specific page upon successful registration

    return render_template("sign_up.html", user=current_user)
