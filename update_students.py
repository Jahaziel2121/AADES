import sqlite3

conn = sqlite3.connect('aades_db.sqlite')
cursor = conn.cursor()

# 1. Update Salamatu and Michael to Information Technology
cursor.execute("UPDATE users SET department = 'Information Technology' WHERE full_name IN ('Amadu Salamatu', 'Annan Abeka Michael');")

# 2. Add Faculties and Programs based on Departments
# IT Department
cursor.execute("""
    UPDATE users 
    SET faculty = 'Faculty of Information Technology and Communication Studies', 
        program = 'BSc. Information Technology' 
    WHERE role = 'student' AND department = 'Information Technology';
""")

# Business Administration Department
cursor.execute("""
    UPDATE users 
    SET faculty = 'Faculty of Management Studies', 
        program = 'BSc. Business Administration' 
    WHERE role = 'student' AND department = 'Business Administration';
""")

# Accounting Department
cursor.execute("""
    UPDATE users 
    SET faculty = 'Faculty of Accounting and Finance', 
        program = 'BSc. Accounting' 
    WHERE role = 'student' AND department = 'Accounting';
""")

conn.commit()

# Print the updated rows
cursor.execute("SELECT full_name, faculty, department, program FROM users WHERE role = 'student';")
rows = cursor.fetchall()
print(f"{'Name':<20} | {'Faculty':<55} | {'Department':<25} | {'Program'}")
print("-" * 130)
for row in rows:
    print(f"{row[0]:<20} | {row[1]:<55} | {row[2]:<25} | {row[3]}")

cursor.close()
conn.close()
