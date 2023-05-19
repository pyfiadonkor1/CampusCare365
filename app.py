from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import datetime
import os


app = Flask(__name__, template_folder="templates", 
            static_folder="templates/static")

app.secret_key = os.urandom(24)
basedir = os.path.abspath(os.path.dirname("app.py"))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'campuscare365.db')
db = SQLAlchemy()
db.init_app(app)

date = datetime.date.today()

class users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date_registered = db.Column(db.Date)
    date_confirmed = db.Column(db.Date)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/signup-login")
def user():
     return render_template('log.html')
  
@app.route("/planner")
def planner():
    return render_template('planner.html')
 
 
@app.route("/meal-mate")
def mealmate():
    return render_template("meal.html")

@app.route("/schedule")
def schedule():
    return render_template("schedule.html") 
 

   
                      
        
            
   
   
   
     
    




if __name__ == "__main__":
    app.run(debug=True)
