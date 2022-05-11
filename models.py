from flask_login import UserMixin
from sqlalchemy.sql import func
from __init__ import db

class Notes(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50),unique=True)
    first_name = db.Column(db.String(30))
    password = db.Column(db.String(30))
    notes = db.relationship(Notes)

