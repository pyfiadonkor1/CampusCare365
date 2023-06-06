from flask import Flask, session, render_template, request, redirect, flash
from model import db, User
import datetime
import os
import sqlalchemy as sa
import smtplib
import random







def create_app():
    app = Flask(__name__, template_folder="templates", 
            static_folder="templates/static")
    app.secret_key = os.urandom(24)
    basedir = os.path.abspath(os.path.dirname("app.py"))
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=30)
    
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = "postgresql://campuscare365:eApbGksp8O5OnG3HS7YgwCaNad2dcJGP@dpg-chgopiak728sd6jvvm2g-a/campuscaredb"
    else:     
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'campuscaredb.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    
    
    db.init_app(app)

    return app



   
app = create_app()
date = datetime.date.today()

 
engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sa.inspect(engine)

if not inspector.has_table("food"):
        with app.app_context():
            db.create_all()
            app.logger.info('Initialized the database!')
            
#if not inspector.has_table("planner"): 
#if not inspector.has_table("user"):           
else:
        app.logger.info('Database already contains the users table.')


    

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/home")
def home():
    if 'email' not in session:
        return redirect('/signup-login')
    user = session['username']
    return render_template('home.html')

@app.route("/signup-login")
def user():
     return render_template('log.html')
  
@app.route("/planner")
def planner():
    if 'email' not in session:
        return redirect('/signup-login')
    return render_template('planner.html')
 
 
@app.route("/meal-mate")
def mealmate():
    if 'email' not in session:
        return redirect('/signup-login')
    return render_template("meal.html")




@app.route('/create_plan', methods=["GET","POST"])
def create():

    if 'email' not in session:
        return redirect('/signup-login')
    return render_template("create_plan.html")



@app.route('/mealplan_generator', methods=["GET","POST"])
def generate_meal_plan():

    if 'email' not in session:
        return redirect('/signup-login')
    return render_template("mealplan_generator.html")

@app.route("/team")
def ourteam():
    if 'email' not in session:
        return redirect('/signup-login')
    return render_template("Our_team.html")

@app.route("/schedule")
def schedule():
    if 'email' not in session:
        return redirect('/signup-login')
    return render_template("schedule.html") 


 
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
        
        
        
        send_verification_email(email)
        
        
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
        
        
        if login_valid(email, password):
            username = login_valid(email,password)
            user = username.split()
            if len(user) >= 2:
                firstname = user[0].capitalize()
            else:
                firstname = username.capitalize()  
            session['username'] = firstname     
            return render_template("home.html", firstname = firstname)
        else:
            flash("Invalid email or password", "error")
            return redirect('/signup-login')
        
    
@app.route('/about')
def about():
    if 'email' not in session:
        return redirect('/signup-login')
    return render_template('about.html')


@app.route('/recipe_search', methods=["GET", "POST"])
def recipe_searching():
    if 'email' not in session:
        return redirect('/signup-login')
    return render_template("recipe_search.html")

def authenticated(username, email):
    user_by_username = User.query.filter_by(username=username).first()
    user_by_email = User.query.filter_by(email=email).first()
    
    if user_by_username and user_by_username.username == username:
        return True
    if user_by_email and user_by_email.email == email:
        return True
    
    return False

   
    
def pass_validation(password,conf_password):
    if str(password) == str(conf_password):
        return True
    return False    
    
def login_valid(email, password, remember_me=True):
    user = User.query.filter_by(email=email).first()
    
    if user and user.password == password:
        session['user_id'] = user.user_id
        session['email'] = user.email
        session['username'] = user.username

        session.permanent = True

        return user.username  

    return None

def send_verification_email(user_email):
    # Generate a verification code
    verification_code = generate_verification_code()
    
    # Email configuration
    sender_email = 'gyamposu@gmail.com'  # Replace with your email address
    sender_password = 'tjoadllrzwrmgzjq'  # Replace with your email password
    subject = 'Email Verification Code from Campuscare365'
    body = f'Your verification code is: {verification_code}'
    
    # Email settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    
    try:
        # Create a secure connection with the SMTP server
       
        server.starttls()
        
        # Login to your email account
        server.login(sender_email, sender_password)
        
        # Create the email message
        message = f'Subject: {subject}\n\n{body}'
        
        # Send the email
        server.sendmail(sender_email, user_email, message)
        
        print('Verification email sent successfully!')
    except Exception as e:
        print(f'An error occurred while sending the verification email: {e}')
    finally:
        # Close the connection
        server.quit()
        
        

def generate_verification_code():
    # Generate a random 6-digit verification code
    return str(random.randint(1000, 9999))
         
        


if __name__ == "__main__":
    app.run(debug=True)



    
    
     #url1 = "https://api.spoonacular.com/mealplanner/generate?timeFrame=day"
    #url = f'https://api.spoonacular.com/mealplanner/generate?timeFrame=day?diet={diet}'
    #request.get(url)``