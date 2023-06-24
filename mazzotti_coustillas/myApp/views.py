from flask import Flask, render_template, redirect, session, request
from .model import bdd
from .controller import function as f
from .controller import hash
import random
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
    listeMembres = bdd.get_membresData()
    print(listeMembres)
    params = { 'liste': listeMembres }
    params = f.messageInfo(params)
    return render_template("administration.html", **params)

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
        session["newMdp"] = user["newMdp"]
        session["mdp"] = user['motPasse']
        session["infoVert"] = "Authentification réussie"
        params=f.messageInfo({})
        if session['newMdp']==0:
            return render_template("surveillance.html", **params) # vers surveillance
        else :
            session["infoBleu"]="Vous devez changer votre mot de passe avant de vous connecter."
            params=f.messageInfo({})
            params["changementmdp"]="Changement de mot de passe nécessaire" #permettra d'afficher le formulaire pour changer le mot de passe dans la page login.html
            return render_template("login.html", **params) # vers login
    except TypeError as err:
        # Authentification refusée
        session["infoRouge"] = "Authentification refusée"
        params=f.messageInfo({})
        return render_template("login.html", **params) # vers page login
    
@app.route("/creationcompte", methods=['POST'])
def creationcompte():
    nom=request.form['nom']
    prenom=request.form['prenom']
    email=request.form['email']
    statut=request.form['statut']
    login=request.form['login']
    mdp=f.generation()
    mdpC=hash.chiffrement(mdp)
    lastId = bdd.add_userData(email, nom, prenom, login, statut, mdpC) #ajoute un membre en BDD
    if "errorDB" not in session:
        session["infoVert"] = "Nouveau membre inséré"
        session["infoBleu"]="Le mot de passe créé pour le nouvel utilisateur est : "+mdp+"."
    else:
        session["infoRouge"] = "Problème ajout membre"
    params=f.messageInfo({})
    return render_template("compte.html", **params) 

@app.route('/nouveaumdp', methods=['POST'])
def changermdp():
    oldmdp=request.form['oldmdp']
    newmdp=request.form['newmdp']
    newmdpconfirmed=request.form['newmdpconfirmed']
    oldmdpC=hash.chiffrement(oldmdp)
    if oldmdpC==session["mdp"]:
        if newmdpconfirmed==newmdp :
            bdd.update_userData('motPasse', hash.chiffrement(newmdp), session['idUser'])
            bdd.update_userData('newMdp', 0, session['idUser'])
            session['newMdp']=0
            session["infoVert"] = "Changement de mot de passe validé"
            params=f.messageInfo({})
            return render_template("surveillance.html", **params)
        else:
            session["infoRouge"] = "Mots de passe renseignés différents"
            params=f.messageInfo({})
            params["changementmdp"]="Changement de mot de passe nécessaire"
            return render_template("login.html", **params)
    else:
        session["infoRouge"] = "Ancien mot de passe erroné"
        params=f.messageInfo({})
        params["changementmdp"]="Changement de mot de passe nécessaire"
        return render_template("login.html", **params)
    