from flask import Flask, session, render_template, request, redirect, flash
from model import db, User
import datetime
import os
import sqlalchemy as sa






def create_app():
    app = Flask(__name__, template_folder="templates", 
            static_folder="templates/static")
    app.secret_key = os.urandom(24)
    basedir = os.path.abspath(os.path.dirname("app.py"))
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=30)
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:     
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'campuscaredb.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    
    


    # Initialize Flask-SQLAlchemy with the Flask application
    db.init_app(app)

    return app


def check_db():
    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            user = User()
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the users table.')

app = create_app()
date = datetime.date.today()
check_dbase = check_db() 



    


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/home")
def home():
    if 'email' not in session:
        return redirect('/signup-login')
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

@app.route("/schedule")
def schedule():
    if 'email' not in session:
        return redirect('/signup-login')
    return render_template("schedule.html") 

@app.route("/fitzone")
def fitzone():
    if 'email' not in session:
        return redirect('/signup-login')
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
            flash("Login successful", "success")
            return redirect('/home')
        else:
            flash("Invalid email or password", "error")
            return redirect('/signup-login')
        
    
"""@app.route('/mealplan_generator', methods=["GET","POST"])
def generate_meal_plan():
    if request.method == 'POST':
        timeFrame = request.form.get("timeFrame")
        targetCalories = request.form.get("targetCalories")
        diet = request.form.get("diet")
        exclude = request.form.get("exclude")
        apiKey = 'bb96fafd19b64b4c86b0f79c917cd7fe'
        URL = f'https://api.spoonacular.com/mealplanner/generate?apiKey={apiKey}&timeFrame={timeFrame}&targetCalories={targetCalories}&diet={diet}&exclude={exclude}'

        response = requests.get(URL)
        if response.status_code == 200:
            meal_plan_data = response.json()
            return render_template("mealGen_results.html", meal_plan_data=meal_plan_data)
        else:
            flash("Error: " + str(response.status_code), "error")
            return redirect("/meal")

    if 'email' not in session:
        return redirect('/signup-login')
    return render_template("mealplan_generator.html")"""



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

    #url1 = "https://api.spoonacular.com/mealplanner/generate?timeFrame=day"
    #url = f'https://api.spoonacular.com/mealplanner/generate?timeFrame=day?diet={diet}'
    #request.get(url)
    
def pass_validation(password,conf_password):
    if str(password) == str(conf_password):
        return True
    return False    
    
def login_valid(email, password, remember_me=True):
    
    user = User.query.filter_by(email=email).first()
    passc = User.query.filter_by(password=password).first()
    
    if user:
        if passc:
            session['user_id'] = user.user_id
            session['email'] = user.email
            session['username'] = user.username
            print(session['username'])
            
            session.permanent = True
            

            return True

    
    return False    
         
        


if __name__ == "__main__":
    app.run(debug=True)
