from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from datetime import datetime



class User(UserMixin, db.Model):
    """
    Create an User table
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    full_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    position = db.Column(db.String(60), index=True)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.id}','{self.email}','{self.username}', '{self.full_name}', '{self.position}')"
    
# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Minutes(db.Model):
    """
    Create an minutes table
    """
    __tablename__ = "minutes"

    minute_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name_of_org = db.Column(db.String(60), index=True, default="analog")
    purpose = db.Column(db.String(60), index=True)
    body = db.Column(db.Text)
    attendees = db.Column(db.String(60), index=True)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    
   
    def _repr_(self):
        return f"Minutes('{self.id}', '{self.title}', '{self.body}', '{self.created_by}','{self.name_of_org}', '{self.purpose}', '{self.date_created}', '{self.date_modified}', '{self.attendees}')"

