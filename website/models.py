# database models
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # when you add a note it will auto add date using func
    # func gets current date and time
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # to associate notes with a user using foreign key
    # a foreign key is essentially a column in your database that always references a column of another database
    # user.id comes from the user class id field
    # one to many relationship. one user many notes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# inherit from db.model and usermixin


class User(db.Model, UserMixin):
    # schema defined
    # define the columns
    # primary key is the unqiue identifier to differentiate
    id = db.Column(db.Integer, primary_key=True)
    # .String sets a max length of string, unique is so no one can have the same email
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # from all users to be able to find all of their notes
    # every time create a note, add into the user's note relationship the note id
    notes = db.relationship('Note')
