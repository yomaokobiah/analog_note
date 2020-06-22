# app/auth/views.py

from flask import flash, redirect, render_template, url_for, request, redirect
from flask_login import login_required, login_user, logout_user

from . import auth
from .. import db
from ..models import User

@auth.route("/signup",methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        position = request.form.get("position")
        confirm_password = request.form.get("confirm_password")
        if User.query.filter_by(username = User.username).first() is None:
            if confirm_password == password:
                user = User(full_name = full_name, username = username,password = password, email = email, position = position)
                # add employee to the database
                db.session.add(user)
                db.session.commit()
                flash('You have successfully registered! You may now login.')

                # redirect to the login page
                return redirect(url_for('auth.login'))
            else:
                return "Password not the same"
        else:
            return "Username taken"

    # load registration template
    return render_template('signup.html',title='Register')

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username = username).first()
        if user is not None and user.verify_password(password):
            # log employee in
            login_user(user, remember=True)
            #return "Successful"
            return redirect(url_for('home.dashboard'))
            
        else:
            flash('Invalid email or password.')
    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))
    
