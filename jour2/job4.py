import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Alep2012..",
    database="LaPlateforme"
)
cursor = conn.cursor()

cursor.execute("SELECT nom, capacite FROM salle")
salles = cursor.fetchall()

print("Liste des salles avec leur capacité :")
for nom, capacite in salles:
    print(f"Salle : {nom}, Capacité : {capacite}")

cursor.close()
conn.close()
