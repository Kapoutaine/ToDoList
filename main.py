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

db = bdd.Bdd(file_name="taches")

results = db.request("get_all_tasks")


# Les routes associées aux fonctions
@app.route("/")
def accueillir():
    """Gère l'accueil des utilisateurs"""
    
    # Rendu de la vue
    return render_template("accueil.html", results=results)

# TODO : ajoutez de nouvelles routes associées à des fonctions "contrôleur" Python


# Lancement du serveur
if __name__ == "__main__":
    """app.run(host="0.0.0.0", port=1664, threaded=True, debug=True)"""

