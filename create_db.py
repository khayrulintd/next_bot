import os.path
import sqlite3



def create_bd():
    connectBD = sqlite3.connect(r'bloodpressure_db.sqlite')    
    connectBD.close()
    


def add_userdata(username, password, role, age, name, surname):
    username = username
    password = password
    role = role
    age = age
    name = name
    surname = surname
    connString = r'bloodpressure_db.sqlite'
    conn = sqlite3.connect(connString)
    cursor = conn.cursor()
    query = f'''
    INSERT INTO users (                      
                      username,
                      password,
                      role,
                      age,
                      name,
                      surname
                  )
                  VALUES (                      
                      '{username}',
                      '{password}',
                      '{role}',
                      '{age}',
                      '{name}',
                      '{surname}'
                  );'''
    cursor.execute(query)    
    conn.commit()
    conn.close()

'''
f = 'test'
global username = 'Vasiliy'
global password = 'qwerty'
global role = 'patient'
global age = 27
global name = 'Vasiliy'
global surname = 'Petrov'
'''



#add_userdata()