from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired

class EditForm(FlaskForm):
    """
    Form for users to edit minutes
    """
    title = StringField('Title', validators=[DataRequired()])
    purpose = StringField('Purpose', validators=[DataRequired()])
    name_of_org = StringField('Organisation', validators=[DataRequired()])
    attendees = StringField('Attendees', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')