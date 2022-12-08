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
    return render_template("accueil.html", results=results)


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


# Lancement du serveur
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1664, threaded=True, debug=True)
