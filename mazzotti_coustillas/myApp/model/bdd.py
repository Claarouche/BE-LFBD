#Vérification de l'authentification des utilisateurs
from . import bddGen 
import hashlib
from ..controller import hash

def verifAuthData(login, mdp):
    mdpC=hash.chiffrement(mdp)
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
    cnx.close()
    return user

#Ajout d'un nouveau compte
def add_userData(email, nom, prenom, login, statut, mdpC):
    cnx = bddGen.connexion()
    if cnx is None: return None
    sql = "INSERT INTO identification (nom, prenom, mail, login, motPasse, statut) VALUES (%s, %s, %s, %s, %s, %s);"
    if statut=="Agent":
       no_statut=2
    elif statut=="Gestionnaire":
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

#Récupération des données de la table identification
def get_membresData():
   cnx = bddGen.connexion()
   if cnx is None: return None
   sql = "SELECT * FROM identification"
   param = None
   msg = {
 "success":"OKmembres",
 "error" : "Failed get membres data"
 }
   listeMembre = bddGen.selectData(cnx, sql, param, msg)
   cnx.close()
   return listeMembre

#Modification du statut d'un utilisateur
def update_statutData(idUser, newvalue):
   cnx = bddGen.connexion()
   if cnx is None: return None
   sql = "UPDATE identification SET statut = %s WHERE login = %s;"
   param = (newvalue, idUser)
   msg = {
"success":"updateMembreOK",
"error" : "Failed update membres data"
}
   bddGen.updateData(cnx, sql, param, msg)
   cnx.close()

#Récupérer la liste des infrastructures
def get_checkpointsData():
   cnx = bddGen.connexion()
   if cnx is None: return None
   sql = "SELECT * FROM checkpoints"
   param = None
   msg = {
 "success":"OKinfra",
 "error" : "Failed get infrastructures data"
 }
   listeInfrastructures = bddGen.selectData(cnx, sql, param, msg)
   cnx.close()
   return listeInfrastructures

#Récupérer une infrastructure en particulier dont on connait l'idCheckpoint:
def get_onecheckpointData(id):
   cnx = bddGen.connexion()
   if cnx is None: return None
   sql = "SELECT * FROM checkpoints WHERE idCheckpoint = %s"
   param = (id,)
   msg = {
 "success":"OKinfra",
 "error" : "Failed get infrastructures data"
 }
   dataInfrastructure = bddGen.selectOneData(cnx, sql, param, msg)
   cnx.close()
   return dataInfrastructure

#Récupérer l'historique d'une infrastructure
def get_onecheckpointHistorique(id):
   cnx = bddGen.connexion()
   if cnx is None: return None
   sql = "SELECT * FROM historique WHERE idCheckpoint = %s"
   param = (id,)
   msg = {
 "success":"OKinfra",
 "error" : "Failed get infrastructures data"
 }
   historiqueInfrastructure = bddGen.selectData(cnx, sql, param, msg)
   cnx.close()
   return historiqueInfrastructure

#Récupérer la liste des infrastructures
def get_historiqueData():
   cnx = bddGen.connexion()
   if cnx is None: return None
   sql = "SELECT * FROM historique"
   param = None
   msg = {
 "success":"OKhisto",
 "error" : "Failed get historique data"
 }
   historique = bddGen.selectData(cnx, sql, param, msg)
   cnx.close()
   return historique

#Ajouter une nouvelle vérification à l'historique
def add_historique(etat, niveau, nature, remarques, idUser, idCheckpoint):
 cnx = bddGen.connexion()
 if cnx is None: return None
 sql = "INSERT INTO historique (etat, niveau, nature, remarques, idUser, idCheckpoint) VALUES (%s, %s, %s, %s, %s, %s);"
 param = (etat, niveau, nature, remarques, idUser, idCheckpoint)
 msg = {
 "success":"addhistoOK",
 "error" : "Failed add historique data"
 }
 lastId = bddGen.addData(cnx, sql, param, msg)
 cnx.close()
 return lastId 

#Ajouter une nouvelle infrastructure
def add_infrastructure(code, nom, type, zone):
 cnx = bddGen.connexion()
 if cnx is None: return None
 sql = "INSERT INTO checkpoints (codeCheckpoint, nomCheckpoint, type, idZone) VALUES (%s, %s, %s, %s);"
 param = (code, nom, type, zone)
 msg = {
 "success":"addinfraOK",
 "error" : "Failed add infrastructure data"
 }
 lastId = bddGen.addData(cnx, sql, param, msg)
 cnx.close()
 return lastId 

#Supprimer une infrastructure
def del_membreData(id):
   cnx = bddGen.connexion()
   if cnx is None: return None
   sql = "DELETE FROM checkpoints WHERE idCheckpoint=%s;"
   param = (id,)
   msg = {
   "success":"suppInfraOK",
   "error" : "Failed del Infrastructures data"
   }
   bddGen.deleteData(cnx, sql, param, msg)
   cnx.close()

#Modifier une infrastructure
def update_InfraData(champ, idCheckpoint, newvalue):
   cnx = bddGen.connexion()
   if cnx is None: return None
   sql = "UPDATE checkpoints SET "+champ+" = %s WHERE idCheckpoint = %s;"
   param = (newvalue, idCheckpoint)
   msg = {
   "success":"updateInfraOK",
   "error" : "Failed update infrastructures data"
   }
   bddGen.updateData(cnx, sql, param, msg)
   cnx.close()

