from flask import Flask, session, render_template, request, redirect, flash
from model import db, User
import datetime
import os
app = Flask(__name__, template_folder="templates", static_folder="templates/static")


app = Flask(__name__, template_folder="templates", 
            static_folder="templates/static")

app.secret_key = os.urandom(24)
basedir = os.path.abspath(os.path.dirname("app.py"))
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'campuscare365.db')

db.init_app(app)

date = datetime.date.today()


    
    


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

@app.route("/fitzone")
def fitzone():
    return render_template("fitzone.html")
 
@app.route("/signup-login", methods=["GET","POST"])
def get_info():
    if 'signup' in request.form:
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        conf_password=request.form['conf_password']
        
        authenticate = authenticated(username, email)
        password_valid = pass_validation(password,conf_password)
        
        if password_valid == False:
            flash("password must match", "error")
            return redirect("/signup-login")
        
        elif authenticate == True:
            flash("Username or Email has been taken", "error")  
            return redirect("/signup-login")
        else:
            new_user = User(username=username,
                            email=email,
                            password=password,
                            date_registered=date)
        
            db.session.add(new_user)
            db.session.commit()
             
        
            return render_template("index.html")
    
    elif 'login' in request.form:
        email=request.form['logemail']
        password=request.form['logpassword']
        
        return render_template("home.html")  
   
   
      
def authenticated(username,email):
    name = User.query.filter_by(username=username).first()
    mail = User.query.filter_by(email=email).first()
    if name == username:
        return True
    elif mail == email:
        return True
    else:
        return False
    
    
def pass_validation(password,conf_password):
    if password == conf_password:
        return True
    else:
        return False    
    
         
    


if __name__ == "__main__":
    app.run(debug=True)
