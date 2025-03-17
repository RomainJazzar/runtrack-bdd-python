import mysql.connector

class Employe:
    def __init__(self):  # Initialise la connexion
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Alep2012..",
            database="employe"
        )
        self.cursor = self.conn.cursor()

    def create(self, nom, prenom, salaire, id_service):  # Ajoute un employé
        query = "INSERT INTO employe (nom, prenom, salaire, id_service) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (nom, prenom, salaire, id_service))
        self.conn.commit()  # Sauvegarde les changements

    def read(self):  # Montre tous les employés
        self.cursor.execute("SELECT * FROM employe")
        return self.cursor.fetchall()

    def update(self, id, salaire):  # Change un salaire
        query = "UPDATE employe SET salaire = %s WHERE id = %s"
        self.cursor.execute(query, (salaire, id))
        self.conn.commit()

    def delete(self, id):  # Supprime un employé
        query = "DELETE FROM employe WHERE id = %s"
        self.cursor.execute(query, (id,))  # Ajout de la virgule pour créer un tuple
        self.conn.commit()

    def close(self):  # Ferme la connexion
        self.cursor.close()
        self.conn.close()

# Test
if __name__ == "__main__":
    emp = Employe()
    
    # Ajoute un employé
    emp.create("Test", "User", 3100.00, 1)
    
    # Montre tous les employés
    print("Tous les employés :")
    for e in emp.read():
        print(e)
    
    # Change le salaire de Jean
    emp.update(1, 4000.00)
    
    # Supprime Sophie
    emp.delete(2)
    
    # Montre ceux avec salaire > 3000
    emp.cursor.execute("SELECT * FROM employe WHERE salaire > 3000")
    print("\nEmployés avec salaire > 3000 :")
    for e in emp.cursor.fetchall():
        print(e)
    
    emp.close()
