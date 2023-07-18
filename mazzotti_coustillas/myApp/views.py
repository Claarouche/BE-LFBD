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
    historique=bdd.get_historiqueData()
    infrastructures=bdd.get_checkpointsData()
    params = { 'listehisto': historique, 'infra' : infrastructures }
    return render_template("surveillance.html",**params)

@app.route("/administration/gestioncomptes")
def gestioncomptes():
    listeMembres = bdd.get_membresData()
    params = { 'liste': listeMembres }
    params["page"]="utilisateur"
    params = f.messageInfo(params)
    return render_template("administration.html", **params)

@app.route("/administration/gestioninfrastructures")
def gestioninfrastructures():
    listeInfrastructures = bdd.get_checkpointsData()
    params = { 'liste': listeInfrastructures }
    params["page"]="infrastructures"
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
            return render_template("index.html", **params) # vers surveillance
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
    
@app.route("/updateStatut", methods=['POST'])
def updateStatut(champ=None):
    idUser = request.form['pk']
    newvalue = request.form['value']
    bdd.update_statutData(idUser, newvalue)
    return "ok"

@app.route("/find/<id>")
def infrastructure(id):
    infrastructures=bdd.get_checkpointsData()
    dataInfrastructure=bdd.get_onecheckpointData(id)
    historiqueInfrastructure=bdd.get_onecheckpointHistorique(id)
    historique=bdd.get_historiqueData()
    params = { 'data': dataInfrastructure, 'histo' : historiqueInfrastructure, 'listehisto': historique, 'infra' : infrastructures }
    return render_template("surveillance.html", **params)

@app.route("/addhistorique", methods=['POST'])
def addhistorique():
    idCheckpoint=request.form['infra']
    etat=request.form['etat']
    niveau=request.form['niveau']
    nature=request.form['nature']
    remarques=request.form['remarques']
    bdd.add_historique(etat, niveau, nature, remarques, session['idUser'], idCheckpoint)
    historique=bdd.get_historiqueData()
    infrastructures=bdd.get_checkpointsData()
    params=f.messageInfo({})
    params['listehisto']= historique
    params['infra'] = infrastructures 
    if "errorDB" not in session:
        session["infoVert"] = "Nouvelle vérification insérée"
    else:
        session["infoRouge"] = "Problème ajout vérification"
    return render_template('surveillance.html',**params)

@app.route('/addinfrastructure', methods=['POST'])
def addinfrastructure():
    code=request.form['code']
    nom=request.form['nom']
    type=request.form['type'] 
    zone=request.form['zone']  
    bdd.add_infrastructure(code, nom, type, zone)
    listeInfrastructures = bdd.get_checkpointsData()
    params=f.messageInfo({})
    params['liste']= listeInfrastructures
    params["page"]="infrastructures"
    if "errorDB" not in session:
        session["infoVert"] = "Nouvelle infrastructure insérée"
    else:
        session["infoRouge"] = "Problème ajout infrastructure"
    return render_template("administration.html", **params)

@app.route('/suppInfra/<id>')
def suppinfrastructure(id):
    bdd.del_membreData(id)
    listeInfrastructures = bdd.get_checkpointsData()
    params=f.messageInfo({})
    params['liste']= listeInfrastructures
    params["page"]="infrastructures"
    if "errorDB" not in session:
        session["infoVert"] = "Infrastructure supprimée"
    else:
        session["infoRouge"] = "Problème suppression infrastructure"
    return render_template("administration.html", **params)

@app.route('/updateInfra/<champ>', methods=['POST'])
def updateinfrastructure(champ):
    idCheckpoint = request.form['pk']
    newvalue = request.form['value']
    if champ == "code":
        bdd.update_InfraData("codeCheckpoint", idCheckpoint, newvalue)
    elif champ == "nom":
        bdd.update_InfraData("nomCheckpoint", idCheckpoint, newvalue)
    elif champ == "type":
        bdd.update_InfraData("type", idCheckpoint, newvalue)
    else:
        bdd.update_InfraData("idZone", idCheckpoint, newvalue)
    return "ok"
