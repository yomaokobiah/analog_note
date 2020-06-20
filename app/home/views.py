# app/home/views.py
from flask_login import login_required, current_user
from flask import flash, redirect, render_template, url_for, request, redirect
from . import home
from ..models import User, Minutes
from app import db
from datetime import datetime

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
    notes = Minutes.query.join(User).add_columns(Minutes.title, Minutes.minute_id, Minutes.purpose, Minutes.name_of_org, User.full_name).all()

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

@home.route('/search', methods = ["POST"])
@login_required
def search_results():
    search_string = request.form.get("search1")
    filter = request.form.get("filters")
    if search_string:
        if filter == 'name_of_org':
            notes = Minutes.query.join(User).add_columns(Minutes.title, Minutes.minute_id, Minutes.purpose, 
            Minutes.name_of_org, User.full_name).filter(Minutes.name_of_org.contains(search_string)).all()
        elif filter == 'purpose':
            notes = Minutes.query.join(User).add_columns(Minutes.title, Minutes.minute_id, Minutes.purpose, 
            Minutes.name_of_org, User.full_name).filter(Minutes.purpose.contains(search_string)).all()
        elif filter == 'attendees':
            notes = Minutes.query.join(User).add_columns(Minutes.title, Minutes.minute_id, Minutes.purpose, 
            Minutes.name_of_org, User.full_name).filter(Minutes.attendees.contains(search_string)).all()
        elif filter == 'date_created':
            date = datetime.strptime(search_string, '%d/%m/%y')
            notes = Minutes.query.join(User).add_columns(Minutes.title, Minutes.minute_id, Minutes.purpose, 
            Minutes.name_of_org, User.full_name).filter(Minutes.date_created.contains(date)).all()       
        else:
            notes = Minutes.query.join(User).add_columns(Minutes.title, Minutes.minute_id, Minutes.purpose, 
            Minutes.name_of_org, User.full_name).all()
    else:
        notes = Minutes.query.join(User).add_columns(Minutes.title, Minutes.minute_id, Minutes.purpose, 
        Minutes.name_of_org, User.full_name).all()
    return render_template('results.html', notes = notes)
   

