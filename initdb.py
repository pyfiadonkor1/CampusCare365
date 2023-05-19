import sqlite3

class DB:

 def __init__(self):
     self.conn = sqlite3.connect('campuscare365.db')
     self.c = self.conn.cursor()

 def user(self):
   conn = self.conn
   c = self.c
   
   c.execute('''CREATE TABLE IF NOT EXISTS "users" (
  "user_id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "username" VARCHAR(50) NOT NULL,
  "password" VARCHAR(100) NOT NULL,
  "email" VARCHAR(100) NOT NULL,       
  "date_registered" DATE,
  "date_confirmed" DATE
  
   )''')

   conn.commit()
   conn.close()
   
   
if __name__ == "__main__":
  user = DB()
  create=user.user()   