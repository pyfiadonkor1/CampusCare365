from flask import Flask, session, render_template, request, redirect

app = Flask(__name__, template_folder="templates", static_folder="templates/static")


userdict={
    "user":{
    "username":"demo",
     "password":"demo",
     "email":"demo@gmail.com"
    }
}


planner={
    "plan":{
        "time":"",
        "date":"" ,
        "todo":""   
        },
    "plan1":{
         "time":"",
        "date":"" ,
        "todo":""   
        },
    "plan3":{
         "time":"",
        "date":"" ,
        "todo":""   
        },
    "plan4":{
         "time":"",
        "date":"" ,
        "todo":""   
        },
    "plan5":{
         "time":"",
        "date":"" ,
        "todo":""   
        }
}

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
 
@app.route("/signup-login", methods=["POST"])
def getinfo():
   
   
    if request.method == "POST":  
         login_email = request.form["email"]
         login_password = request.form["password"]
         userdictionary = userdict["user"]
         print("login")
         if login_email == "demo@gmail.com":
             if login_password == "demo":
               
               
              return redirect("/home")
                 
         
    elif request.method == "POST":
                   
      username = request.form["username"]
      email = request.form["email"]
      password = request.form["password"]
      con_password = request.form["conf_password"]
      
      if password != con_password:
          msg = "password do not match"
          return render_template("/signup-login", msg=msg)
      else:
          userdictionary = userdict["user"]
          userdictionary["username"] = username 
          userdictionary["email"] = email
          userdictionary["password"] = password
          
      return redirect("/signup-login")
      
      
     
    


if __name__ == "__main__":
    app.run(debug=True)
