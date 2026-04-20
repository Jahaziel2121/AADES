import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('aades_db.sqlite')
cursor = conn.cursor()

# Set Godwin's password
cursor.execute("UPDATE users SET password_hash = ? WHERE email = 'godwin@upsamail.edu.gh'", 
               (generate_password_hash('lecturer123', method='pbkdf2:sha256'),))

# Set everyone else's password to password123
cursor.execute("UPDATE users SET password_hash = ? WHERE role = 'supervisor' AND email != 'godwin@upsamail.edu.gh'", 
               (generate_password_hash('password123', method='pbkdf2:sha256'),))

conn.commit()
cursor.close()
conn.close()
print("All supervisor passwords have been standardized.")
