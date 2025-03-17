import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Alep2012..",
    database="LaPlateforme"
)
cursor = conn.cursor()

cursor.execute("SELECT SUM(superficie) FROM etage")
total_superficie = cursor.fetchone()[0]

print(f"La superficie de La Plateforme est de {total_superficie} m2")

cursor.close()
conn.close()
