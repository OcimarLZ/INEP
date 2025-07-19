import sqlite3

conn = sqlite3.connect('INEP.db')
conn.text_factory = bytes  # Força leitura como bytes para examinar o encoding
cursor = conn.cursor()
cursor.execute("SELECT * FROM regiao LIMIT 5")
for row in cursor.fetchall():
    print(row)
conn.close()
