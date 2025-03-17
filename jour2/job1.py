import mysql.connector

# Remplacez par vos identifiants de connexion
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Alep2012..",
    database="laplateforme"
)

cursor = conn.cursor()

# Supposons que la table des étudiants s'appelle "etudiant"
cursor.execute("SELECT * FROM etudiant")
etudiants = cursor.fetchall()

print("Liste des étudiants :")
for etu in etudiants:
    print(etu)

cursor.close()
conn.close()
