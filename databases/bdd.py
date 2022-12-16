"""Mini-projet ToDoList - squelette de départ

Ce mini-projet en terminale NSI consiste à créer une application web dynamique
gérant une liste de tâches à faire
"""

# Librairie(s) utilisée(s)
import sqlite3
import datetime


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
AND Taches.idPriorite = Priorite.idPriorite;
                                        """,
                                       "get_sorted": """
SELECT Taches.titre, Categorie.nom, Taches.dateEcheance
FROM Taches
INNER JOIN Categorie, Priorite
ON Categorie.idCategorie = Taches.idCategorie
WHERE Taches.idPriorite != 3;
                                        """,
                                       "add": """
INSERT INTO Taches
(titre, idCategorie, idPriorite, dateEcheance)
VALUES (?, ?, ?, ?);
                                        """,
                                       "delete": """
DELETE FROM Taches
WHERE Taches.idTache = ?;
                                """,
                                       "update": """
UPDATE Taches
SET Taches.titre = ?, Taches.idCategorie = ?, Taches.idEtat = ?,
Taches.idPriorite = ?, Taches.dateEcheance = ?
WHERE Taches.idTache = ?;
                                """}

    def task_sort(self, result):
        result.sort(key=lambda l: self.get_remaining_time(l[0]))
        return result

    @staticmethod
    def get_remaining_time(date):
        """
        Calculate how many days we are from a given date
        """

        date = date.split(sep="-")
        date = datetime.date(int(date[0]), int(date[1]), int(date[2]))

        today = datetime.date.today()

        delta = date - today

        return delta.days

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

        if choice == "get_sorted_tasks":
            results = self.task_sort(results)

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
