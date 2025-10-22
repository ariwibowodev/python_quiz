from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import pytz

TIMEZONE = pytz.timezone('Asia/Jakarta')

def convert_to_local_time(dt_utc):
    """Mengkonversi objek datetime dari UTC ke GMT+7 (Asia/Jakarta)"""
    if dt_utc is None:
        return None
    dt_utc = pytz.utc.localize(dt_utc)
    return dt_utc.astimezone(TIMEZONE)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    daily_results = db.relationship('DailyResult', backref='author', lazy='dynamic')
    scores = db.relationship('Scoreboard', backref='player', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class DailyResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    result_data = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def local_date(self):
        return convert_to_local_time(self.date)
    
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), index=True, unique=True)
    answer_a = db.Column(db.String(200))
    answer_b = db.Column(db.String(200))
    answer_c = db.Column(db.String(200))
    answer_d = db.Column(db.String(200)) 
    correct_answer = db.Column(db.String(1)) 

class Scoreboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    high_score = db.Column(db.Integer, default=0)
    last_quiz_date = db.Column(db.DateTime)

    @property
    def local_last_quiz_date(self):
        return convert_to_local_time(self.last_quiz_date)