"""Mini-projet ToDoList - squelette de départ

Ce mini-projet en terminale NSI consiste à créer une application web dynamique
gérant une liste de tâches à faire
"""

# Librairie(s) utilisée(s)
import sqlite3


# La classe
class Bdd:
    """Classe pour faire le lien entre la base de données SQLite et le programme"""

    def __init__(self, file_name: str):
        """
        Initialize the class and open DB
        :param file_name: string
        """
        self.path = f"databases/{file_name}.sqlite"

        # Open the database
        self.database = sqlite3.connect(database=self.path, check_same_thread=False)

        # Creating a dictionary which contains the sql requests
        self.sql_request_dictionary = {"get_all": """
SELECT 
Taches.titre, Categorie.nom, Etat.nom,
Priorite.nom, Taches.dateEcheance, Taches.dateFin,
CAST((julianday(Taches.dateEcheance) - julianday('now')) as INT),
Taches.idTache
FROM Taches
INNER JOIN Categorie, Etat, Priorite
WHERE Taches.idCategorie = Categorie.idCategorie
AND Taches.idEtat = Etat.idEtat
AND Taches.idPriorite = Priorite.idPriorite;""",
                                       "get_sorted_by_date": """
SELECT
Taches.titre, Categorie.nom, Etat.nom,
Priorite.nom, Taches.dateEcheance, Taches.dateFin,
CAST((julianday(Taches.dateEcheance) - julianday('now')) as INT) as tempsRestant,
Taches.idTache
FROM Taches
INNER JOIN Categorie, Etat, Priorite
ON Taches.idCategorie = Categorie.idCategorie
AND Taches.idEtat = Etat.idEtat
AND Taches.idPriorite = Priorite.idPriorite
WHERE Taches.idCategorie != ?
AND Taches.idEtat != ?
AND Taches.idEtat != ?
AND Taches.idPriorite != ?
AND Taches.idPriorite != ?
ORDER BY tempsRestant ASC;""",
                                       "get_sorted": """
SELECT
Taches.titre, Categorie.nom, Etat.nom,
Priorite.nom, Taches.dateEcheance, Taches.dateFin,
CAST((julianday(Taches.dateEcheance) - julianday('now')) as INT) as tempsRestant,
Taches.idTache
FROM Taches
INNER JOIN Categorie, Etat, Priorite
ON Taches.idCategorie = Categorie.idCategorie
AND Taches.idEtat = Etat.idEtat
AND Taches.idPriorite = Priorite.idPriorite
WHERE Taches.idCategorie != ?
AND Taches.idEtat != ?
AND Taches.idEtat != ?
AND Taches.idPriorite != ?
AND Taches.idPriorite != ?;""",
                                       "add": """
INSERT INTO Taches
(titre, idCategorie, idPriorite, dateEcheance)
VALUES (?, ?, ?, ?);""",
                                       "delete": """
DELETE FROM Taches
WHERE Taches.idTache = ?;""",
                                       "update": """
UPDATE Taches
SET titre = ?, idCategorie = ?, idEtat = ?,
idPriorite = ?, dateEcheance = ?, dateFin = ?
WHERE idTache = ?;"""}

    def request(self, choice: str, parameters=None):
        """
        Create a command and execute it
        :param choice: string
        :param parameters: list
        :return: string
        """

        # Open the database
        # self.database = sqlite3.connect(database=self.path)

        # Creating the parameters list if needed

        if parameters is None:
            parameters = []

        results = []

        try:
            command = self.sql_request_dictionary[str(choice)]
        except KeyError:
            return "Choice does not exist"

        results += self.execute(command=command, parameters=parameters)

        return results

    def execute(self, command, parameters):
        """
        Execute a sql request
        :param command: string
        :param parameters: Iterable
        :return: tuple
        """
        cursor = self.database.cursor()  # Placing cursor
        result_list = cursor.execute(command, parameters)  # Execute a sql request

        self.database.commit()

        return result_list.fetchall()


# Mise au point de la classe Bdd seule
if __name__ == "__main__":
    data_base = Bdd(file_name="taches")
    # data_base.request("add", ["Faire les devoirs",1,1, "2022/08/16", ])
    my_result = data_base.request("get_all")
    print(my_result)
