from flask import session

def messageInfo(params = {}):
    if "infoVert" in session:
        params["infoVert"] = session['infoVert']
        session.pop("infoVert",None)
    if "infoRouge" in session:
        params["infoRouge"] = session['infoRouge']
        session.pop("infoRouge", None)
    if "infoBleu" in session:
        params["infoBleu"] = session['infoBleu']
        session.pop("infoBleu", None)
    if "errorDB" in session:
        params["errorDB"] = session['errorDB']
        session.pop("errorDB", None)
    if "successDB" in session:
        params["successDB"] = session['successDB']
        session.pop("successDB", None)
    return params
