ENV = "development"
DEBUG = True
SEND_FILE_MAX_AGE_DEFAULT = 0 #vider le cache
SECRET_KEY="maCleSuperSecurisee"

#Configuration du serveur web
WEB_SERVER = {
    "host": "localhost",
    "port":8080,
}
#Configuration du serveur de BDD
DB_SERVER = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "port": 3306, 
    "database": "gsea22a_mazzotti_coustillas", #nom de la BDD
    "raise_on_warnings": True
}

COLOR ={
'header' : '\033[95m',
'blue' : '\033[94m',
'green' : '\033[92m',
'orange' : '\033[93m',
'red' : '\033[31m',
'end' : '\033[0m',
}