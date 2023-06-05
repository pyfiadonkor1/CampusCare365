from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date_registered = db.Column(db.Date)
    date_confirmed = db.Column(db.Date)
    

class Planner(db.Model):
    __tablename__ = 'planner'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50))
    date = db.Column(db.Date)
    details = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('planners', lazy=True))
    

class Food(db.Model):
    __tablename__ = 'food'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000))
    image = db.Column(db.String(1000))
    details = db.Column(db.String(1000))
    

