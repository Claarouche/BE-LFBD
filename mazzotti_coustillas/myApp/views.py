from flask import Flask, render_template, redirect, session, request
from .model import bdd
from .controller import function as f
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

@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")

@app.route("/nouveaucompte")
def nouveaucompte():
    return render_template("compte.html")

@app.route("/connecter", methods=["POST"])
def connecter():
    login = request.form['login']
    password = request.form['password']
    user = bdd.verifAuthData(login, password)
    try:
    # Authentification réussie
        session["idUser"] = user["idUser"]
        session["nom"] = user["nom"]
        session["prenom"] = user["prenom"]
        session["mail"] = user["mail"]
        session["statut"] = user["statut"]
        session["infoVert"] = "Authentification réussie"
        params=f.messageInfo({})
        return render_template("index.html", **params) # vers page accueil
    except TypeError as err:
        # Authentification refusée
        session["infoRouge"] = "Authentification refusée"
        params=f.messageInfo({})
        return render_template("login.html", **params) # vers page login