"""Mini-projet ToDoList - squelette de départ

Ce mini-projet en terminale NSI consiste à créer une application web dynamique
gérant une liste de tâches à faire
"""

# Librairie(s) utilisée(s)
import sqlite3
import os
import datetime


# La classe
class Bdd:
    """Classe pour faire le lien entre la base de données SQLite et le programme"""

    def __init__(self, file_name: str):
        """
        Initialize the class and open DB
        :param file_name: string
        """
        self.path = os.path.abspath(f"{file_name}.sqlite")

        # Open the database
        self.database = sqlite3.connect(database=self.path)

        # Creating a dictionary which contains the sql requests
        self.sql_request_dictionary = {"1": """
SELECT Taches.titre, Categorie.nom, Taches.dateEcheance
FROM Taches
INNER JOIN Categorie, Priorite
ON Categorie.idCategorie = Taches.idCategorie
WHERE Taches.idPriorite != 3;
                                        """,
                                       "2": """
INSERT INTO Taches
(titre, idCategorie, idPriorite, dateEcheance)
VALUES (?, ?, ?, ?);
                                        """,
                                       "3": """
DELETE FROM Taches
WHERE Taches.titre = ?;
                                """,
                                       "4": """
UPDATE Taches
SET Taches.? = "valeur"
WHERE ?;
                                        """}

    def task_sort(self, result):
        result.sort(key=lambda l: l[0])

    def get_remaining_time(self, date):
        


    def create_command(self, id_choice: int, parameters=None):
        """
        :param id_choice: integer
        :param parameters: list
        :return: string
        """
        # Creating the parameters list if needed

        if parameters is None:
            parameters = []

        results = []

        try:
            command = self.sql_request_dictionary[str(id_choice)]
        except KeyError:
            return "Choice does not exist"

        if id_choice == 3:
            results += self.execute(command=command[0], parameters=parameters)
            results += self.execute(command=command[1], parameters=parameters)
            return results

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

        return result_list


# Mise au point de la classe Bdd seule
if __name__ == "__main__":
    data_base = Bdd(file_name="taches")
    my_result = data_base.create_command(1)
    for row in my_result:
        print(row)

    print(str(datetime.datetime.now())[:10])
