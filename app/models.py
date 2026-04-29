from app import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(30),nullable=False)
    section=db.Column(db.String(5),nullable=False)

class Timetable(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    section=db.Column(db.String(20),nullable=False)
    day=db.Column(db.String(20),nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    slot = db.Column(db.String(20), nullable=False)
    def __repr__(self):
       return f"{self.day} - {self.subject} ({self.slot})"
    
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    timetable_id = db.Column(db.Integer, db.ForeignKey('timetable.id'))
    timetable = db.relationship('Timetable')
    date = db.Column(db.Date)
    status = db.Column(db.String(10))  # Present / Absent

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    subject = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    present = db.Column(db.Integer, nullable=False)

class Holiday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100))
    start_date=db.Column(db.Date)
    end_date=db.Column(db.Date)
