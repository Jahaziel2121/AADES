import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('aades_db.sqlite')
cursor = conn.cursor()

new_students = [
    # Information Technology
    ('Kofi Adjei', '10341111@upsamail.edu.gh', 'Information Technology', 'Faculty of Information Technology and Communication Studies', 'BSc. Information Technology'),
    ('Akosua Serwaa', '10342222@upsamail.edu.gh', 'Information Technology', 'Faculty of Information Technology and Communication Studies', 'BSc. Information Technology'),
    ('Kwabena Owusu', '10343333@upsamail.edu.gh', 'Information Technology', 'Faculty of Information Technology and Communication Studies', 'BSc. Information Technology'),
    ('Ama Osei', '10344444@upsamail.edu.gh', 'Information Technology', 'Faculty of Information Technology and Communication Studies', 'BSc. Information Technology'),
    ('Yaw Boakye', '10345555@upsamail.edu.gh', 'Information Technology', 'Faculty of Information Technology and Communication Studies', 'BSc. Information Technology'),
    ('Yaa Asantewaa', '10346666@upsamail.edu.gh', 'Information Technology', 'Faculty of Information Technology and Communication Studies', 'BSc. Information Technology'),
    ('Kofi Mensah', '10347777@upsamail.edu.gh', 'Information Technology', 'Faculty of Information Technology and Communication Studies', 'BSc. Information Technology'),
    
    # Business Administration
    ('Afia Kusi', '10348888@upsamail.edu.gh', 'Business Administration', 'Faculty of Management Studies', 'BSc. Business Administration'),
    ('Kwame Nkrumah', '10349999@upsamail.edu.gh', 'Business Administration', 'Faculty of Management Studies', 'BSc. Business Administration'),
    ('Abena Appiah', '10351010@upsamail.edu.gh', 'Business Administration', 'Faculty of Management Studies', 'BSc. Business Administration'),
    ('Kwasi Addo', '10352020@upsamail.edu.gh', 'Business Administration', 'Faculty of Management Studies', 'BSc. Business Administration'),
    ('Akua Danso', '10353030@upsamail.edu.gh', 'Business Administration', 'Faculty of Management Studies', 'BSc. Business Administration'),
    ('Akwasi Frimpong', '10354040@upsamail.edu.gh', 'Business Administration', 'Faculty of Management Studies', 'BSc. Business Administration'),
    ('Yaa Agyeiwaa', '10355050@upsamail.edu.gh', 'Business Administration', 'Faculty of Management Studies', 'BSc. Business Administration'),
    
    # Accounting
    ('Kwaku Manu', '10356060@upsamail.edu.gh', 'Accounting', 'Faculty of Accounting and Finance', 'BSc. Accounting'),
    ('Esi Ofori', '10357070@upsamail.edu.gh', 'Accounting', 'Faculty of Accounting and Finance', 'BSc. Accounting'),
    ('Kwadwo Asamoah', '10358080@upsamail.edu.gh', 'Accounting', 'Faculty of Accounting and Finance', 'BSc. Accounting'),
    ('Ama Nyarko', '10359090@upsamail.edu.gh', 'Accounting', 'Faculty of Accounting and Finance', 'BSc. Accounting'),
    ('Yaw Koomson', '10360000@upsamail.edu.gh', 'Accounting', 'Faculty of Accounting and Finance', 'BSc. Accounting'),
    ('Abena Gyamfi', '10361111@upsamail.edu.gh', 'Accounting', 'Faculty of Accounting and Finance', 'BSc. Accounting'),
]

password_hash = generate_password_hash('student123', method='pbkdf2:sha256')

for name, email, dept, faculty, program in new_students:
    try:
        cursor.execute('''
            INSERT INTO users (full_name, email, password_hash, role, status, department, faculty, program, student_id)
            VALUES (?, ?, ?, 'student', 'active', ?, ?, ?, ?)
        ''', (name, email, password_hash, dept, faculty, program, email.split('@')[0]))
    except sqlite3.IntegrityError:
        pass # Skip if already exists

conn.commit()
cursor.close()
conn.close()
print("Added 20 new students.")
