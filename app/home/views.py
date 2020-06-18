# app/home/views.py
from flask_login import login_required, current_user
from flask import flash, redirect, render_template, url_for, request, redirect
from . import home
from ..models import User, Minutes
from app import db

@home.route('/')
@home.route('/home')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    notes = Minutes.query.add_columns(Minutes.title, Minutes.minute_id, Minutes.purpose, Minutes.name_of_org).all()

    return render_template('dashboard.html', title="Dashboard", notes = notes)

@home.route('/handle_data', methods=["GET", "POST"])
@login_required
def handle_data():
    
    title = request.form.get("title")
    body = request.form.get("body")
    org = request.form.get("org")
    purpose = request.form.get("purpose")
    attendees = request.form.get("attendees")
    user = current_user.get_id()
    # user = session["user_id"]
    minute = Minutes(body = body, name_of_org =org, purpose = purpose, 
                    attendees = attendees, created_by = user, title=title)
    db.session.add(minute)
    db.session.commit()
    flash("You have create a note")

    return redirect(url_for('home.dashboard'))
   

