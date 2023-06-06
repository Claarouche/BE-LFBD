#Vérification de l'authentification des utilisateurs
from . import bddGen 
import hashlib

def verifAuthData(login, mdp):
    mdp=hashlib.sha256(mdp.encode())
    mdpC=mdp.hexdigest()
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