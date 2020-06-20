from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, TextField
from wtforms.validators import DataRequired

class EditForm(FlaskForm):
    """
    Form for users to edit minutes
    """
    title = StringField('title', validators=[DataRequired()])
    purpose = StringField('purpose', validators=[DataRequired()])
    name_of_org = StringField('name_of_org', validators=[DataRequired()])
    attendees = StringField('attendees', validators=[DataRequired()])
    body = TextField('body', validators=[DataRequired()])
    submit = SubmitField('submit')