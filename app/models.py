from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    habits = db.relationship('Habit', cascade='all, delete', backref='user')
    checks = db.relationship('Check', cascade='all, delete', backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Habit(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(120), index=True)
    notes = db.Column(db.Text)
    custom_schedule = db.Column(db.Boolean, default=False)
    days = db.Column(db.String(7))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) ##
    checks = db.relationship('Check', cascade='all, delete', backref='habits')

    def __repr__(self):
        return '<Habit {}>'.format(self.name)

class Check(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, index=True)

    def __repr__(self):
        return '<Check {} {}>'.format(self.habit_id, self.date)


db.create_all()
db.session.commit()
