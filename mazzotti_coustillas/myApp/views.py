from flask import Flask, render_template, redirect, session
app = Flask(__name__)
app.template_folder = "template"
app.static_folder = "static"
app.config.from_object('myApp.config')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/surveillance")
def surveillance():
    return render_template("surveillance.html")

@app.route("/administration")
def administration():
    return render_template("administration.html")

@app.route("/webmasters")
def webmasters():
    return render_template("webmasters.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/nouveaucompte")
def nouveaucompte():
    return render_template("compte.html")