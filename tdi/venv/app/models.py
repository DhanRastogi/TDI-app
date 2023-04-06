from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    ashoka_id = db.Column(db.Integer, nullable=True, unique=True)
    name = db.Column(db.String, nullable=True, index=True)
    #phone_number=db.Column(db.Integer, nullable=True, index=True)
    ashoka_email = db.Column(db.String, nullable=True, index=True, unique=True)
    flat_number=db.Column(db.String, nullable=True, index=True)
    room_number=db.Column(db.Integer, nullable=True, index=True)
    #occupation=db.Column(db.String, nullable=False, index=True)
    #course=db.Column(db.String, nullable=True, index=True)
    #department=db.Column(db.String, nullable=False, index=True)
    password_hash = db.Column(db.String, nullable=True)
    hk_requests = db.relationship('Housekeeping_Request', backref='resident', lazy='dynamic' )

    def __repr__(self):
        return 'User {}'.format(self.ashoka_id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 

class Housekeeping_Request(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    ashoka_id = db.Column(db.Integer, db.ForeignKey('user.ashoka_id'), nullable=True)
    time_slot = db.Column(db.String, nullable=True)
    body = db.Column(db.String, nullable=True)
        
    def __repr__(self):
      return 'Request {}'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


    

