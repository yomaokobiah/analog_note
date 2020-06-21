from flask_login import login_required, 
from flask import flash, redirect, render_template, url_for, request, redirect
from . import notes
from ..models import User, Minutes
from app import db
from datetime import datetime
from .edit_form import EditForm





@notes.route('/note/<int:n_id>', methods=["GET"])
@login_required
def view_note(n_id):
    note = Minutes.query.join(User).add_columns(Minutes.created_by,Minutes.body,Minutes.title, Minutes.purpose, Minutes.minute_id, Minutes.name_of_org, Minutes.attendees, Minutes.date_created, Minutes.date_modified, User.full_name).filter(Minutes.minute_id == n_id).first()
    user = User.query.add_column(User.full_name).filter_by(id=note.created_by)
    create = note.date_created.strftime("%d of %B %Y on %A at %I:%M %p")
    modified = note.date_modified.strftime("%d of %B %Y on %A at %I:%M %p")
    
    return render_template("note.html", note = note, modified=modified, user=user,create = create)

@notes.route('/delete/<int:d_id>', methods=['GET'])
@login_required
def delete_note(d_id):
    minute = Minutes.query.filter_by(minute_id=d_id).first()
    db.session.delete(minute)
    db.session.commit()
    flash('You have successfully deleted a note')

    # redirect to the departments page
    return redirect(url_for('home.dashboard'))

@notes.route("/edit/<int:e_id>", methods=["GET", "POST"])
@login_required
def edit_note(e_id):
    note = Minutes.query.filter(Minutes.minute_id==e_id).first()
    note_dict = {"title": note.title, "body": note.body,"minute_id": note.minute_id, "attendees": note.attendees, "purpose": note.purpose, "name_of_org": note.name_of_org}
    form = EditForm(data=note_dict)
    
    if request.method == "POST":
        note.title = form.title.data
        note.purpose = form.purpose.data
        note.name_of_org = form.name_of_org.data
        note.attendees = form.attendees.data
        note.body = form.body.data
        db.session.commit()
        flash('You have successfully edited the note.')

        # redirect to the departments page
        return redirect(url_for('notes.view_note',n_id=note.minute_id))
        
    
            
    return render_template('edit_form.html', action="Edit",note=note, form=form,title="Edit Note")


