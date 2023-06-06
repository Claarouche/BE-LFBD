#Chiffrement des mots de passe

import hashlib

mdp='mermoz'
mdp=hashlib.sha256(mdp.encode())
mdpC=mdp.hexdigest() #mot de passe chiffré
print(mdpC)