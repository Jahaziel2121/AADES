# create_users.py
from werkzeug.security import generate_password_hash
import mysql.connector

# --------------------------
# MySQL Connection
# --------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mysqlp@$$w0rd",
    database="aades_db"
)
cursor = db.cursor()

# --------------------------
# Users to create
# --------------------------
users = [
    {
        "full_name": "Amu Julius",
        "email": "amu.julius@example.com",
        "password": generate_password_hash("student123"),
        "role": "student"
    },
    {
        "full_name": "Amadu Salamatu",
        "email": "amadu.salamatu@example.com",
        "password": generate_password_hash("student123"),
        "role": "student"
    },
    {
        "full_name": "Annan Abeka Michael",
        "email": "annan.abeka@example.com",
        "password": generate_password_hash("student123"),
        "role": "student"
    },
    {
        "full_name": "Mr Godwin Ntow Danso",
        "email": "godwin@example.com",
        "password": generate_password_hash("lecturer123"),
        "role": "lecturer"
    }
]

# --------------------------
# Insert users into database
# --------------------------
for user in users:
    cursor.execute("""
        INSERT INTO users (full_name, email, password_hash, role, status)
        VALUES (%s, %s, %s, %s, 'active')
    """, (user['full_name'], user['email'], user['password'], user['role']))
    print(f"Created user: {user['full_name']}")

db.commit()
cursor.close()
db.close()
print("All users have been added successfully.")
