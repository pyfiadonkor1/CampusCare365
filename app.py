from flask import Flask, render_template, request
app = Flask('__name__')

@app.get('/')
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/process", methods=['POST'])
def process_login():
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']
    return 'Hello, {}! Your email is {}.'.format(name, email)

if __name__ == '__main__':
    app.run(debug=True)
