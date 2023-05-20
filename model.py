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