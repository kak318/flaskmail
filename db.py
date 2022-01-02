import sqlite3, random

def create_table():
    conn = sqlite3.connect("flormail.db")
    cursor = conn.cursor()
    query = "DROP TABLE IF EXISTS users"
    cursor.execute(query)
    conn.commit()

    query = "CREATE TABLE users(username VARCHAR UNIQUE, password VARCHAR, email VARCHAR)"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def create_inbox():
    conn = sqlite3.connect("flormail.db")
    cursor = conn.cursor()
    query = "DROP TABLE IF EXISTS mail"
    cursor.execute(query)
    conn.commit()

    query = "CREATE TABLE mail(fromu VARCHAR, tou VARCHAR, content VARCHAR, title VARCHAR, id VARCHAR)"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def add_user(username, password, email):
    conn = sqlite3.connect("flormail.db")
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
    cursor.execute(query, (username, password, email,))
    conn.commit()
    cursor.close()
    cursor.close()

def check_user(username, password):
    conn = sqlite3.connect("flormail.db")
    cursor = conn.cursor()
    query = 'SELECT * FROM users WHERE username = ? AND password = ?'
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.commit()
    return result
    cursor.close()
    conn.close()

def login(u, p):
  conn = sqlite3.connect("flormail.db")
  cursor = conn.cursor()
  username = u
  password = p
  if check_user(username, password):
      return True
  else:
      return False
  cursor.close()
  conn.close()

def list_users():
  conn = sqlite3.connect("flormail.db")
  cursor = conn.cursor()
  query = 'SELECT * FROM users'
  cursor.execute(query)
  result = cursor.fetchall()
  conn.commit()
  return result
  cursor.close()
  conn.close()

def check_user_pn(username):
  conn = sqlite3.connect("flormail.db")
  cursor = conn.cursor()
  query = 'SELECT * FROM users WHERE username = ?'
  cursor.execute(query, (username,))
  result = cursor.fetchone()
  conn.commit()
  return result
  cursor.close()
  conn.close()

def check_email(username):
  conn = sqlite3.connect("flormail.db")
  cursor = conn.cursor()
  query = 'SELECT * FROM users WHERE username = ?'
  cursor.execute(query, (username,))
  result = cursor.fetchone()
  conn.commit()
  return result[2]
  cursor.close()
  conn.close()

def inbox(email):
  conn = sqlite3.connect("flormail.db")
  cursor = conn.cursor()
  query = 'SELECT * FROM mail WHERE tou = ?'
  cursor.execute(query, (email,))
  result = cursor.fetchall()
  conn.commit()
  return result
  cursor.close()
  conn.close()

def send(fromu, tou, content, title, id):
  conn = sqlite3.connect("flormail.db")
  cursor = conn.cursor()
  query = 'INSERT INTO mail (fromu, tou, content, title, id) VALUES (?, ?, ?, ?, ?)'
  cursor.execute(query, (fromu, tou, content, title, id,))
  result = cursor.fetchone()
  conn.commit()
  return result
  cursor.close()
  conn.close()

def Reverse(tuples):
  new_tup = tuples[::-1]
  return new_tup

def get_mail_by_id(id_):
  conn = sqlite3.connect("flormail.db")
  cursor = conn.cursor()
  query = 'SELECT * FROM mail WHERE id = ?'
  cursor.execute(query, (id_,))
  result = cursor.fetchone()
  conn.commit()
  return result
  cursor.close()
  conn.close()

def rand():
  char = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
  mlen = 50
  r = ''
  for i in range(mlen):
    r = r + char[random.randint(0, len(char) - 1)]
  return r

def sent(email):
  conn = sqlite3.connect("flormail.db")
  cursor = conn.cursor()
  query = 'SELECT * FROM mail WHERE fromu = ?'
  cursor.execute(query, (email,))
  result = cursor.fetchall()
  conn.commit()
  return result
  cursor.close()
  conn.close()

def check_pass(password, user):
  conn = sqlite3.connect("flormail.db")
  cursor = conn.cursor()
  query = 'SELECT * FROM users WHERE username = ?'
  cursor.execute(query, (user,))
  result = cursor.fetchone()
  conn.commit()
  return result
  cursor.close()
  conn.close()

def update_pass(newpassword, user):
  conn = sqlite3.connect("flormail.db")
  cursor = conn.cursor()
  query = 'UPDATE users SET password = ? WHERE username = ?'
  cursor.execute(query, (newpassword, user,))
  result = cursor.fetchone()
  conn.commit()
  return result
  cursor.close()
  conn.close()

def del_account(user):
  conn = sqlite3.connect("flormail.db")
  cursor = conn.cursor()
  query = 'DELETE FROM users WHERE username = ?'
  cursor.execute(query, (user,))
  result = cursor.fetchone()
  conn.commit()
  return result
  cursor.close()
  conn.close()

