#Vérification de l'authentification des utilisateurs
from . import bddGen 
import hashlib
from ..controller import hash

def verifAuthData(login, mdp):
    mdpC=hash.chiffrement(mdp)
    print(mdpC)
    cnx = bddGen.connexion()
    if cnx is None: return None
    sql = "SELECT * FROM identification WHERE login=%s and motPasse=%s"
    param=(login, mdpC)
    msg = {
    "success":"authOK",
    "error" : "Failed get Auth data"
    }
    # requête par fetchone
    user = bddGen.selectOneData(cnx, sql, param, msg)
    print(user)
    cnx.close()
    return user

#Ajout d'un nouveau compte
def add_userData(email, nom, prenom, login, statut, mdpC):
    cnx = bddGen.connexion()
    if cnx is None: return None
    sql = "INSERT INTO identification (nom, prenom, mail, login, motPasse, statut) VALUES (%s, %s, %s, %s, %s, %s);"
    if statut=="Agent" or statut=="Gestionnaire":
       no_statut=1
    else:
       no_statut=0
    param = (nom, prenom, email, login, mdpC, no_statut)
    msg = {
 "success":"addMembreOK",
 "error" : "Failed add membres data"
 }
    lastId = bddGen.addData(cnx, sql, param, msg)
    cnx.close()
    return lastId 

#Modification d'un utilisateur
def update_userData(champ, newValue, idUser):
    cnx = bddGen.connexion()
    if cnx is None: return None
    sql = "UPDATE identification SET "+champ+" = %s WHERE idUser = %s;"
    param = (newValue, idUser)
    msg = {
 "success":"updateMembreOK",
 "error" : "Failed update membres data"
 }
    bddGen.updateData(cnx, sql, param, msg)
    cnx.close()