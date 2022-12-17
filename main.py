"""Mini-projet ToDoList - squelette de départ

Ce mini-projet en terminale NSI consiste à créer une application web dynamique
gérant une liste de tâches à faire
"""

# Librairie(s) utilisée(s)
from flask import *
from databases import bdd
import secrets


# Création des objets Flask et Bdd
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Obtentions des tâches de la base de données

database = bdd.Bdd(file_name="taches")

results = database.request("get_all")


# Fonctions pratiques
def maj():
    """Retourne les nouvelles taches apres la mise a jour de la base de données"""
    new_results = database.request("get_all")

    return new_results


# Les routes associées aux fonctions
@app.route("/")
def accueillir():
    """Gère l'accueil des utilisateurs"""

    # Rendu de la vue
    return render_template("accueil.html", results=maj())


@app.route("/supprimer", methods=["POST"])
def supprimer():
    """Supprime un tache de la base de données"""
    id_tache = request.form["idTache"]

    database.request("delete", parameters=[id_tache, ])
    return render_template("accueil.html", results=maj())


@app.route("/ajouter", methods=["POST"])
def ajouter():
    """Ajoute une tache"""

    parameters = \
        [request.form["name"], request.form["categorie"], request.form["priorite"], request.form["date_echeance"], ]

    database.request("add", parameters=parameters)

    return render_template("accueil.html", results=maj())


@app.route("/modifier", methods=["POST"])
def modifier():
    """Modifie une tache"""

    parameters = \
        [request.form["name"], request.form["categorie"],
         request.form["etat"], request.form["priorite"],
         request.form["date_echeance"], request.form["date_fin"], ]

    tache = request.form["tache"][1:-1].split(sep=", ")

    for i in range(len(tache)):
        if tache[i][0] == "'":
            tache[i] = tache[i][1:-1]

    del tache[-2]

    for j in range(len(parameters)):
        if parameters[j] != tache[j] and parameters[j] != '':
            tache[j] = parameters[j]

    if tache[-2] is None:
        tache[-2] = ""

    print(parameters, tache)

    database.request("update", parameters=tache)

    return render_template("accueil.html", results=maj())


@app.route("/ouvrir_modfier", methods=["POST"])
def ouvrir_modifier():
    """Ouvre la page pour modifier une tache"""

    tache = request.form["tache"][1:-1].split(sep=", ")

    for i in range(len(tache)):
        if tache[i][0] == "'":
            tache[i] = tache[i][1:-1]

    return render_template("modifier.html", tache=tache)


@app.route("/tri", methods=["POST"])
def tri():
    """Trie les taches en fonction du choix de l'utilisateur"""

    parameters = \
        [request.form["categorie"], request.form["etat"], ] + request.form["priorite"].split(sep=",")

    parameters.insert(2, request.form.get(key="archivee", default=0))

    if request.form.get("sorted") == 1:
        sorted_results = database.request("get_sorted_by_date", parameters=parameters)
    else:
        sorted_results = database.request("get_sorted", parameters=parameters)

    return render_template("accueil.html", results=sorted_results)


# Lancement du serveur
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1664, threaded=True, debug=True)
