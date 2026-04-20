import sqlite3
from werkzeug.security import generate_password_hash

departments = ['Information Technology', 'Business Administration', 'Accounting']
new_supervisors = [
    # IT
    ('Dr. Alan Turing', 'alan.turing@upsamail.edu.gh', 'Information Technology'),
    ('Dr. Ada Lovelace', 'ada.lovelace@upsamail.edu.gh', 'Information Technology'),
    ('Prof. Linus Torvalds', 'linus.torvalds@upsamail.edu.gh', 'Information Technology'),
    # Business
    ('Dr. Philip Kotler', 'philip.kotler@upsamail.edu.gh', 'Business Administration'),
    ('Prof. Michael Porter', 'michael.porter@upsamail.edu.gh', 'Business Administration'),
    ('Dr. Peter Drucker', 'peter.drucker@upsamail.edu.gh', 'Business Administration'),
    # Accounting
    ('Dr. Luca Pacioli', 'luca.pacioli@upsamail.edu.gh', 'Accounting'),
    ('Prof. Arthur Andersen', 'arthur.andersen@upsamail.edu.gh', 'Accounting'),
    ('Dr. Charles Waldo', 'charles.waldo@upsamail.edu.gh', 'Accounting')
]

conn = sqlite3.connect('aades_db.sqlite')
cursor = conn.cursor()

# Ensure all students have a department (fallback just in case)
cursor.execute("UPDATE users SET department = 'Information Technology' WHERE role = 'student' AND (department IS NULL OR department = '')")

# Insert 3 new supervisors per department
for full_name, email, dept in new_supervisors:
    # Check if exists
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (full_name, email, password_hash, role, status, department)
            VALUES (?, ?, ?, 'supervisor', 'active', ?)
        ''', (full_name, email, generate_password_hash('password123', method='pbkdf2:sha256'), dept))
        print(f"Added supervisor: {full_name} ({dept})")

conn.commit()
cursor.close()
conn.close()
print("Database seeded with new supervisors.")
