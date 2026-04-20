from werkzeug.security import generate_password_hash

print("Student password hash:", generate_password_hash("student123"))
print("Lecturer password hash:", generate_password_hash("lecturer123"))
print("Admin password hash:", generate_password_hash("admin123"))
