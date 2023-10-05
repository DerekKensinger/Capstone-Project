# Import necessary modules and packages
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Define the 'Note' model for storing user notes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each note
    data = db.Column(db.String(10000))  # Stores the actual note data (up to 10,000 characters)
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # Timestamp of when the note was created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key linking the note to a user

# Define the 'User' model for storing user information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user
    email = db.Column(db.String(150), unique=True)  # User's email address (unique constraint)
    password = db.Column(db.String(150))  # Hashed password for user authentication
    first_name = db.Column(db.String(150))  # User's first name
    notes = db.relationship('Note')  # Establish a one-to-many relationship with 'Note' model
