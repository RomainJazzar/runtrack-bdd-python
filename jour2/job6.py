import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Alep2012..",
    database="LaPlateforme"
)
cursor = conn.cursor()

cursor.execute("SELECT SUM(capacite) FROM salle")
total_capacite = cursor.fetchone()[0]

print("La capacité totale des salles est de", total_capacite)

cursor.close()
conn.close()
