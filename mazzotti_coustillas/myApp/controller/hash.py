import hashlib

#Chiffrement des mots de passe
def chiffrement(mdp):
    mdp=hashlib.sha256(mdp.encode())
    mdpC=mdp.hexdigest() #mot de passe chiffré
    return mdpC