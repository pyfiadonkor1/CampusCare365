from flask import Flask, session, render_template, request, redirect

app = Flask(__name__, template_folder="templates", static_folder="templates/static")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template('home.html')




if __name__ == "__main__":
    app.run(debug=True)
