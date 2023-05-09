import sqlite3

conn = sqlite3.connect('myapp.db')
c = conn.cursor()

c.execute('''CREATE TABLE "users" (
  "user_id" INT AUTO_INCREMENT,
  "first_name" VARCHAR(50) NOT NULL,
  "last_name" VARCHAR(50) NOT NULL,
  "password" VARCHAR(100) NOT NULL,
  PRIMARY KEY (user_id)
)''')

conn.commit()
conn.close()