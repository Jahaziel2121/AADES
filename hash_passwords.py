# hash_passwords.py
from werkzeug.security import generate_password_hash
import mysql.connector

# ---------------- MYSQL CONNECTION ----------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysqlp@$$w0rd",  # <-- replace with your real password
        database="aades_db"
    )

# ---------------- USERS & PASSWORDS ----------------
users = {
    "amu@example.com": "student123",
    "amadu@example.com": "student123",
    "annan@example.com": "student123",
    "godwin@example.com": "lecturer123"
}

# ---------------- UPDATE PASSWORDS ----------------
conn = get_db_connection()
cursor = conn.cursor()

for email, password in users.items():
    hashed = generate_password_hash(password)
    query = "UPDATE users SET password_hash = %s WHERE email = %s"
    cursor.execute(query, (hashed, email))
    print(f"Updated password for {email}")

conn.commit()
cursor.close()
conn.close()
print("All passwords updated successfully!")
