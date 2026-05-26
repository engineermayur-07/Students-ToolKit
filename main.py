# Developing a student toolkit for a school management system which has the
# following features:
# 1. Student Registration: Allow students to register by providing their name, age, grade, and contact information.
# 2, Features students to add the tasks they want to accomplish
# 3. View Tasks: Students can view their list of tasks and mark them as completed.
#4.Students can get resources for studying, such as links to educational websites, study materials, and tips for effective studying.
import sqlite3
import sys

# --- DATABASE SETUP ---
# Connect to the database file and create the table if it's missing
conn = sqlite3.connect('student_toolkit.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        email TEXT PRIMARY KEY,
        name TEXT,
        password TEXT,
        age INTEGER,
        class TEXT,
        contact_info TEXT
    )
''')
conn.commit()
conn.close()


# --- FUNCTIONS ---

def student_Registration():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    
    # Connect to check if email exists
    conn = sqlite3.connect('student_toolkit.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT email FROM students WHERE email = ?", (email,))
    if cursor.fetchone():
        print("❌ Email already registered. Please sign in.")
        conn.close()
        return

    age = input("Enter your age: ")
    class_ = input("Enter your class: ")
    contact_info = input("Enter your mobile no:  ")
    
    cursor.execute('''
        INSERT INTO students (email, name, password, age, class, contact_info) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (email, name, password, age, class_, contact_info))
    
    conn.commit()
    conn.close()
    print(f"\n🎉 Student '{name}' registered successfully!")


def reset_password(email):
    conn = sqlite3.connect('student_toolkit.db')
    cursor = conn.cursor()
    
    # Fetch student details for verification
    cursor.execute("SELECT contact_info FROM students WHERE email = ?", (email,))
    result = cursor.fetchone()
    
    if result:
        db_contact = result[0]
        contact = input("Enter your registered mobile number: ")
        
        if contact != db_contact:
            print("❌ Incorrect contact information. Password reset failed.")
            conn.close()
            return 
            
        new_password = input("Enter your new password: ")
        # Update the password in the database
        cursor.execute("UPDATE students SET password = ? WHERE email = ?", (new_password, email))
        conn.commit()
        print("✅ Password reset successful.")
    else:
        print("❌ Email not found. Please register first.")
        
    conn.close()

def profile(email):
    conn=sqlite3.connect("student_toolkit.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM students WHERE email=?", (email,))
    result=cursor.fetchone()
    if result:
        print("✅ Profile found!")
        print(f"Name :  {result[1]}")
        print(f"Age :  {result[3]}")
        print(f"Class :  {result[4]}")
        print(f"Contact Info : { result[5]}")
    else:
        print("❌ Profile not found.")
    conn.close()
 


def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    
    conn = sqlite3.connect('student_toolkit.db')
    cursor = conn.cursor()
    
    # Search for a row matching BOTH email and password
    cursor.execute("SELECT * FROM students WHERE email = ? AND password = ?", (email, password))
    student = cursor.fetchone()
    conn.close()
    
    if student:
        print(f"\n✅ Login successful! Welcome back.")
        return student,True  
    else:
        print("❌ Invalid email or password.")
        forgot_password = input("Forgot password? (yes/no): ")
        if forgot_password.lower() == 'yes':
            reset_password(email)
        else:
            return login() # Re-run login if they say no


# --- MAIN TERMINAL LOOP ---
while True:
    print("\nWelcome to the Student Toolkit")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")
    
    if choice == '1' or choice.lower() == "register":
        student_Registration()
    elif choice == '2' or choice.lower() == "login":
        student,logged_in=login()
        if logged_in:
            print("\n--- Main Application Menu coming next! ---")
            while True:
                print(f"Welcome {student[1]}! What would you like to do?")
                print("1. View Profile")
                print("2. Schedule Tasks")
                print("3. Delete Tasks")
                print("4. Logout")
                sub_choice = input("Enter your choice: ")
                if sub_choice == '1' or sub_choice.lower() == "view profile":
                    profile(student[0])
                elif sub_choice == '2' or sub_choice.lower() == "schedule tasks":
                    print("Scheduling tasks feature coming soon!")
                elif sub_choice == '3' or sub_choice.lower() == "delete tasks":
                    print("Delete tasks feature coming soon!")
                elif sub_choice == '4' or sub_choice.lower() == "logout":
                    print("Logging out...")
                    break

            
    elif choice == '3' or choice.lower() == "exit":
        print("Exiting the Student Toolkit. Goodbye!")
        sys.exit()
    else:
        print("Invalid choice. Please try again.")