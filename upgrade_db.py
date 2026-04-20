import sqlite3

def upgrade_db():
    conn = sqlite3.connect("aades_db.sqlite")
    cursor = conn.cursor()
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "faculty" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN faculty TEXT")
        print("Added 'faculty' column.")
    if "department" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN department TEXT")
        print("Added 'department' column.")
    if "program" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN program TEXT")
        print("Added 'program' column.")
        
    conn.commit()
    conn.close()
    print("Database upgraded successfully!")

if __name__ == "__main__":
    upgrade_db()
