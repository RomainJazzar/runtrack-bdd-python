import mysql.connector

class ZooManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Alep2012..",
            database="zoo"
        )
        self.cursor = self.conn.cursor()

    def ajouter_animal(self):
        nom = input("Nom de l’animal : ")
        race = input("Race : ")
        id_cage = int(input("ID de la cage : "))
        date_naissance = input("Date de naissance (YYYY-MM-DD) : ")
        pays = input("Pays d’origine : ")
        query = "INSERT INTO animal (nom, race, id_cage, date_naissance, pays_origine) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (nom, race, id_cage, date_naissance, pays))
        self.conn.commit()

    def supprimer_animal(self):
        id = int(input("ID de l’animal à supprimer : "))
        self.cursor.execute("DELETE FROM animal WHERE id = %s", (id,))
        self.conn.commit()

    def modifier_animal(self):
        id = int(input("ID de l’animal à modifier : "))
        nom = input("Nouveau nom : ")
        self.cursor.execute("UPDATE animal SET nom = %s WHERE id = %s", (nom, id))
        self.conn.commit()

    def ajouter_cage(self):
        superficie = int(input("Superficie de la cage : "))
        capacite = int(input("Capacité max : "))
        self.cursor.execute("INSERT INTO cage (superficie, capacite_max) VALUES (%s, %s)", (superficie, capacite))
        self.conn.commit()

    def afficher_animaux(self):
        self.cursor.execute("SELECT * FROM animal")
        print("Animaux dans le zoo :")
        for animal in self.cursor.fetchall():
            print(animal)

    def afficher_animaux_par_cage(self):
        self.cursor.execute("SELECT c.id, c.superficie, a.nom FROM cage c LEFT JOIN animal a ON c.id = a.id_cage")
        print("Animaux par cage :")
        for row in self.cursor.fetchall():
            print(row)

    def superficie_totale(self):
        self.cursor.execute("SELECT SUM(superficie) FROM cage")
        total = self.cursor.fetchone()[0] or 0  # Si aucune cage, renvoie 0
        print(f"Superficie totale des cages : {total} m²")

    def menu(self):
        while True:
            choix = input("\n1. Ajouter animal\n2. Supprimer animal\n3. Modifier animal\n4. Ajouter cage\n5. Afficher animaux\n6. Afficher animaux par cage\n7. Superficie totale\n8. Quitter\nChoix : ")
            if choix == "1": self.ajouter_animal()
            elif choix == "2": self.supprimer_animal()
            elif choix == "3": self.modifier_animal()
            elif choix == "4": self.ajouter_cage()
            elif choix == "5": self.afficher_animaux()
            elif choix == "6": self.afficher_animaux_par_cage()
            elif choix == "7": self.superficie_totale()
            elif choix == "8": break

    def close(self):
        self.cursor.close()
        self.conn.close()

# Lance le programme
if __name__ == "__main__":
    zoo = ZooManager()
    zoo.menu()
    zoo.close()