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

# Define a list of recipes with their related information
recipes = [
        {
            'name': 'Jollof Rice',
            'ingredients': ['2 cups long-grain rice', '1 onion,ﬁnely chopped', '2 tomatoes, blended or ﬁnely chopped', '1 red bell pepper, blended or ﬁnely chopped', '1 scotch bonnet pepper or habanero pepper,ﬁnely chopped(adjust according to your spice preference)', '3 cloves of garlic, minced', '1 teaspoon thyme', '1 teaspoon curry powder', '1teaspoonpaprika', '1 teaspoon dried thyme', '1 teaspoon dried parsley', '2 tablespoons tomato paste', '3 tablespoons vegetable oil', '2 cups chicken or vegetable broth', 'Salt to taste', 'Optional: 1 cup of mixed vegetables(carrots, peas, bell peppers)'],
            'instructions': [
                "Rinse the rice under cold water until the water runs clear. Drain and set aside.",
                "Heat the vegetable oil in a large pot or Dutch oven over medium heat.",
                "Add the chopped onions and sauté until they become translucent.",
                "Stir in the minced garlic, blended tomatoes, blended red bell pepper, and chopped scotch bonnet pepper. Cook for about 5 minutes, allowing the mixture to reduce slightly.",
                "Add the tomato paste, thyme, curry powder, paprika, dried thyme, dried parsley, and salt. Stir well to combine and cook for another 3-4 minutes.",
                "Add the rice to the pot and stir until it is well coated with the tomato mixture.",
                "Pour in the chicken or vegetable broth and bring to a boil. Reduce the heat to low, cover the pot, and let it simmer for about 20-25 minutes, or until the rice is cooked and all the liquid has been absorbed. If using mixed vegetables, add them to the pot during the last 5 minutes of cooking.",
                "Once the rice is cooked, fluff it gently with a fork.",
                "Remove from heat and let it rest for a few minutes before serving."
                            ],
            'nutrients': ['Calories: 300', 'Protein: 10g', 'Carbs: 50g', 'Fat: 5g']
        },

        {
            'name': 'Noodles',
            'ingredients': ['chicken breast', 'bell peppers', 'zucchini', 'olive oil', 'salt', 'pepper'],
                "instructions": [
        "Cook the noodles according to the package instructions until they are al dente. Drain and set aside.",
        "Heat the vegetable oil in a large skillet or wok over medium-high heat.",
        "Add the minced garlic and sliced onion to the skillet and stir-fry for about 1-2 minutes until fragrant and the onion becomes translucent.",
        "Add the julienned carrot, sliced bell pepper, shredded cabbage, and broccoli florets to the skillet. Stir-fry for about 3-4 minutes or until the vegetables are tender-crisp.",
        "Push the vegetables to one side of the skillet and add the cooked noodles to the other side.",
        "Drizzle the soy sauce and oyster sauce (if using) over the noodles and toss everything together to combine. Stir-fry for another 2-3 minutes until the noodles are heated through and well coated with the sauce.",
        "Optional: Drizzle sesame oil over the noodles and toss again to add extra flavor.",
        "Season with salt and pepper to taste. Adjust the seasoning and sauce quantities based on your preference.",
        "Remove from heat and transfer the stir-fried noodles to serving plates or bowls.",
        "Garnish with sliced green onions, toasted sesame seeds, or chopped cilantro, if desired.",
        "Serve the noodles hot as a main dish or as a side dish with your choice of protein."
    ],
            'nutrients': ['Calories: 250', 'Protein: 25g', 'Carbs: 10g', 'Fat: 12g']
        }
        
]

# Define the route that will display the recipe information
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
       
       
        server.starttls()
        
        
        server.login(sender_email, sender_password)
        
        
        message = f'Subject: {subject}\n\n{body}'
        
       
        server.sendmail(sender_email, user_email, message)
        
        print('Verification email sent successfully!')
    except Exception as e:
        print(f'An error occurred while sending the verification email: {e}')
    finally:
        
        server.quit()
        
        

def generate_verification_code():
    
    return str(random.randint(1000, 9999))
         
        


if __name__ == "__main__":
    app.run(debug=True)



    
    
     #url1 = "https://api.spoonacular.com/mealplanner/generate?timeFrame=day"
    #url = f'https://api.spoonacular.com/mealplanner/generate?timeFrame=day?diet={diet}'
    #request.get(url)``