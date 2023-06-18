from flask import Flask, session, render_template, request, redirect, flash, make_response
from model import db, User
from recipe import recipes
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
     return render_template("index.html", show_success=False)
    

@app.route("/home")
def home():
    if 'email' not in session:
        return redirect('/signup-login')
    firstname = session['username']  
    firstname = firstname.capitalize()    
             
    return render_template('home.html', firstname=firstname)

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




@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = recipes[recipe_id]
    return render_template('recipe.html', recipe_name=recipe['name'], ingredients=recipe['ingredients'], instructions=recipe['instructions'], nutrients=recipe['nutrients'])


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
        
        
        
       
        
        
        new_user = User(username=username,
                        email=email,
                        password=password,
                        date_registered=date)
        
        db.session.add(new_user)
        db.session.commit()
        session['signed_up'] = True
             
        
        return render_template("index.html")
    
    elif 'login' in request.form:
        email=request.form['logemail']
        password=request.form['logpassword']
        
        
        if login_valid(email, password):
            username = login_valid(email,password)
            user = username.split(" ")
            if len(user) >= 2:
                firstname = user[0].capitalize()
            else:
                firstname = username.capitalize()  
            session['username'] = firstname 
             
          
                
            
   
            return redirect("/home")
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

@app.route('/edit-profile')
def edit_profile():
    if 'email' not in session:
        return redirect('/signup-login')
    session['update'] = False
    return render_template('profile.html')

@app.route('/edit-profile', methods=["GET", "POST"])
def edit_profile_info():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        
        print(fullname + email + password)
        
        if fullname == "":
            fullname = None
        if email  == "":
            email = None
        if password == "":
            password = None        
        
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        
        if fullname and email and password:
            user.email = email
            user.username = fullname
            user.password = password
            session['update'] = True
        
        elif  email and fullname:
            user.email = email
            user.username = fullname 
            session['update'] = True
        
        elif email and password:
            user.email = email       
            user.password = password
            session['update'] = True
        
        elif fullname and password:
            user.username = fullname
            user.password = password
            session['update'] = True
        
        else:
            if password and fullname == None == email:
                user.password = password
            elif fullname and password == None == email:
                user.username = fullname
                print("vut")
            elif email and not any(request.form.values()):
                user.email = email
            session['update'] = True
        session['user_id'] = user.user_id
        session['email'] = user.email
        session['username'] = user.username    
    db.session.commit()    
                                     
        
    return redirect('/home')

@app.route('/verify', methods=["GET","POST"])
def verify():
    if 'email' not in session:
        return redirect('/signup-login')
    email = session['email']
    ver = send_verification_email(email)
    code1 = str(request.form['code1'])
    code2 = str(request.form['code2'])
    code3 = str(request.form['code3'])
    code4 = str(request.form['code4'])
    code = (code1+code2+code3+code4)
    
    if code == ver:
        msg = ("success")
        return redirect("/home")
    
    return render_template('verification.html')

@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect('/signup-login')
    return render_template('profilepage.html')


    
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect("/signup-login")


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
    verification_code = generate_verification_code()
    # Email configuration
    sender_email = 'gyamposu@gmail.com'  
    sender_password = 'tjoadllrzwrmgzjq'  
    subject = 'Email Verification Code from Campuscare365'
    body = f'Your verification code is: {verification_code}'
    
    # Email settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    
    
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        
        server.login(sender_email, sender_password)
        
        
        message = f'Subject: {subject}\n\n{body}'
        
       
        server.sendmail(sender_email, user_email, message)
        
        print('Verification email sent successfully!')
        
        server.quit()
        return verification_code
        
    except Exception as e:
        print(f'An error occurred while sending the verification email: {e}')
    
        
        
        
        

def generate_verification_code():
    
    return str(random.randint(1000, 9999))
         
        


if __name__ == "__main__":
    app.run(debug=True)



    
    
    #url1 = "https://api.spoonacular.com/mealplanner/generate?timeFrame=day"
    #url = f'https://api.spoonacular.com/mealplanner/generate?timeFrame=day?diet={diet}'
    #request.get(url)``