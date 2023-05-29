import sqlite3

class DB:

 def __init__(self):
     self.conn = sqlite3.connect('campuscare365.db')
     self.c = self.conn.cursor()

 def user(self):
   conn = self.conn
   c = self.c
   
   c.execute('''CREATE TABLE IF NOT EXISTS "user" (
  "user_id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "username" VARCHAR(50) NOT NULL,
  "password" VARCHAR(100) NOT NULL,
  "email" VARCHAR(100) NOT NULL,       
  "date_registered" DATE,
  "date_confirmed" DATE
  
   )''')

   conn.commit()
   conn.close()
   
 def food(self):
    conn = self.conn
    c = self.c
    
    c.execute('''CREATE TABLE IF NOT EXISTS "food" (
      "food_name" VARCHAR(100),
      "description" VARCHAR(250)
      
    )''')
    
    conn.commit()
    conn.close()
    
 def drinks(self):
   conn = self.conn
   c = self.c
   
   c.execute('''CREATE TABLE IF NOT EXISTS "drink" (
     "drink_name" VARCHAR(100),
     "description" VARCHAR(250)
   )''')   
   
   
   conn.commit()
   conn.close()
   
 def snacks(self):
   conn =self.conn
   c = self.c
   
   c.execute('''CREATE TABLE IF NOT EXISTS "snacks(
     "snack_name" VARCHAR(100),
     "description" VARCHAR(250)
   )''')  
   
   
   conn.commit()
   conn.close()
   
   
if __name__ == "__main__":
  user = DB()
  usertable = user.user()
  foodtable = user.food()
  snacktable = user.snacks()
  drinkstable = user.drinks()
     