import mysql.connector

# ---------------- MYSQL CONNECTION ----------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysqlp@$$w0rd",  # <-- your actual MySQL password
        database="aades_db"
    )

# ---------------- CHECK TABLE ----------------
def describe_table(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DESCRIBE {table_name};")
    rows = cursor.fetchall()
    print(f"Columns in '{table_name}' table:")
    for row in rows:
        print(row)
    cursor.close()
    conn.close()

# Run the check
if __name__ == "__main__":
    describe_table("submissions")
