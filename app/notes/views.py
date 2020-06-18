from flask_login import login_required, current_user
from flask import flash, redirect, render_template, url_for, request, redirect
from . import notes
from ..models import User, Minutes
from app import db

@notes.route('/note/<int:n_id>', methods=["GET"])
@login_required
def view_note(n_id):
    note = Minutes.query.add_columns(Minutes.created_by,Minutes.body,Minutes.title, Minutes.purpose, Minutes.minute_id, Minutes.name_of_org, Minutes.attendees, User.full_name).filter_by(minute_id=n_id).first()
    user = User.query.add_column(User.full_name).filter_by(id=note.created_by)
    return render_template("note.html", note = note, user = user)

@notes.route('/delete/<int:d_id>', methods=['GET'])
@login_required
def delete_note(d_id):
    minute = Minutes.query.filter_by(minute_id=d_id).first()
    db.session.delete(minute)
    db.session.commit()
    flash('You have successfully deleted a note')

    # redirect to the departments page
    return redirect(url_for('home.dashboard'))

