import sqlite3

def upgrade_db_section():
    conn = sqlite3.connect("aades_db.sqlite")
    cursor = conn.cursor()
    
    # Check if column already exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "section" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN section TEXT")
        print("Added 'section' column.")
        
    conn.commit()
    conn.close()
    print("Database upgraded successfully with section!")

if __name__ == "__main__":
    upgrade_db_section()
