# Developing a student toolkit for a school management system which has the
# following features:
# 1. Student Registration: Allow students to register by providing their name, age, grade, and contact information.
# 2, Features students to add the tasks they want to accomplish
# 3. View Tasks: Students can view their list of tasks and mark them as completed.
#4.Students can get resources for studying, such as links to educational websites, study materials, and tips for effective studying.
import sqlite3
import sys
import json
resources_={
         "documentation":{
            "c language":"https://www.cprogramming.com/tutorial/c-tutorial.html",
            "python":"https://www.python.org/doc/",
            "java":"https://docs.oracle.com/en/java/",
            "javascript":"https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
            "html":"https://developer.mozilla.org/en-US/docs/Web/HTML",
            "css":"https://developer.mozilla.org/en-US/docs/Web/CSS",
            "sql":"https://www.w3schools.com/sql/"  ,
            "sqlite":"https://www.sqlite.org/docs.html",
            "git":"https://git-scm.com/doc"
         },
         "notes":{
            "html":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/YouTube/The%20Ultimate%20HTML%20handbook.pdf",
            "css":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/notes/CSS_Complete_Notes.pdf",
            "javascript":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/notes/JS_Chapterwise_Notes.pdf",
            "php":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/cheatsheets/Php%20Cheatsheet.pdf",
            "c programming":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/YouTube/The%20Ultimate%20C%20Handbook.pdf",
            "c++":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/cheatsheets/C%2B%2B%20Cheatsheet.pdf",
            "java":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/notes/Java_Complete_Notes.pdf",
            "python":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/YouTube/The%20Ultimate%20Python%20Handbook.pdf",
            "dsa":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/notes/DSA_CompleteNotes.pdf",
            "sql":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/YouTube/MySQL%20Handbook.pdf",
            "mysql":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/cheatsheets/MySQL%20Cheatsheet.pdf",
            "mongodb":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/YouTube/MongoDB%20Handbook.pdf",
            "django":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/cheatsheets/Django%20Cheatsheet.pdf",
            "flask":"https://cwh-full-next-space.fra1.cdn.digitaloceanspaces.com/cheatsheets/Flask%20Cheatsheet.pdf"
         }
          
    }

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

conn=sqlite3.connect("student_toolkit.db")
cursor=conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_email TEXT,
        task TEXT,
        completed INTEGER DEFAULT 0,
        deadline TEXT,
        FOREIGN KEY (student_email) REFERENCES students (email)
    )
''')
conn.commit()
conn.close()


# --- FUNCTIONS ---

def resources():
    print("---RESOURCES---")
    for category in resources_:
        print(f"\n{category.upper()} :")
        for topic  in resources_[category]:
            print(f"{topic} : {resources_[category][topic]}")
        print(20*"-")


def date_checker(date):
    try:
        day, month, year = map(int, date.split('-'))
        if 1 <= day <= 31 and 1 <= month <= 12 and year > 0:
            if month == 2:
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                    if day <= 29:
                        return True
                    else:
                        return False
                else:
                    if day <= 28:
                         return True
                    else:
                        return False
            return True
        else:
            return False
    except ValueError:
        return False

def student_Registration():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    
    # Connect to check if email exists
    conn = sqlite3.connect('student_toolkit.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT email FROM students WHERE email = ?", (email,))
    if cursor.fetchone():
        print("❌ Email already registered. Please sign in.")
        conn.close()
        return
    password = input("Enter your password: ")
    if not password_checker(password):
        print("❌ Invalid password. Please try again.")
        return student_Registration()
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

def password_checker(password):
    if len(password) < 8:
        print("❌ Password must be at least 8 characters long.")
        return False
    if not any(char.isdigit() for char in password):
        print("❌ Password must contain at least one digit.")
        return False
    if not any(char.isalpha() for char in password):
        print("❌ Password must contain at least one letter.")
        return False
    return True

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
        if not password_checker(new_password):
            print("❌ Invalid password. Please try again.")
            conn.close()
            return reset_password(email)
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
        print(50*"=")
        print("\t\t-- Student Profile --\n")
        print(f"Name :  {result[1]}")
        print(f"Age :  {result[3]}")
        print(f"Class :  {result[4]}")
        print(f"Contact Info : { result[5]}")
        print(50*"=")
    else:
        print("❌ Profile not found.")
    conn.close()
 
def schedule_task(email):
    task=input("Enter the task you want to schedule :- ")
    deadline=input("Enter the deadline for the task (DD-MM-YYYY): ").strip()
    if not date_checker(deadline):
        print("❌ Invalid date format. Please enter the date in DD-MM-YYYY format.")
        return schedule_task(email)
    conn=sqlite3.connect("student_toolkit.db")
    cursor=conn.cursor()
    cursor.execute('''
        INSERT INTO tasks(student_email,task,deadline) VALUES(?,?,?)
    ''',(email,task,deadline))
    print("✅ Task scheduled successfully!")
    conn.commit()
    conn.close()

def view_tasks(email):
    conn=sqlite3.connect("student_toolkit.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE student_email = ?", (email,))
    tasks=cursor.fetchall()
    if tasks:
        print(50*"=")
        print("\t\t-- Tasks --")
        for task in tasks:
            print(f"Task: {task[2]}, Deadline: {task[4]}")
        print(50*"=")
    else:
        print("❌ No tasks found.")
    conn.close()

def delete_tasks(email):
    conn=sqlite3.connect("student_toolkit.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE student_email = ?", (email,))
    tasks=cursor.fetchall()
    if tasks:
        
        print("✅ Tasks found!")
        
        for task in tasks:
            print(f"ID: {task[0]}, Task: {task[2]}, Deadline: {task[4]}")
        task_id=input("Enter the ID of the task you want to delete: ")
        cursor.execute("DELETE FROM tasks WHERE id = ? AND student_email = ?", (task_id, email))
        conn.commit()
        print("✅ Task deleted successfully.")
    else:
        print("❌ No tasks found.")
    conn.close()

def Completed_tasks(email):
    conn=sqlite3.connect("student_toolkit.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE student_email = ? and completed = 0", (email,))
    tasks=cursor.fetchall()
    if tasks:
        print("✅ Following are incomplete Tasks!")
        for task in tasks:
            print(f"ID: {task[0]}, Task: {task[2]}, Deadline: {task[4]}, Completed: {task[3]}")
        task_id=input("Enter the ID of the task you want to mark as completed: ")
        cursor.execute("UPDATE tasks SET completed = TRUE WHERE id = ? AND student_email = ?", (task_id, email))
        conn.commit()
        print("✅ Task is marked as completed.")
    else:
        print("❌ No tasks found.")
    conn.close()

def view_completed_tasks(email):
    conn=sqlite3.connect("student_toolkit.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE student_email = ? and completed = 1", (email,))
    tasks=cursor.fetchall()
    if tasks:
        print(50*"=")
        print("✅ Following are completed Tasks!")
        for task in tasks:
            print(f"ID: {task[0]}, Task: {task[2]}, Deadline: {task[4]}, Completed: {task[3]}")
        print(50*"=")
    else:
        print("❌ No completed tasks found.")
    conn.close()

def view_incomplete_tasks(email):
    conn=sqlite3.connect('student_toolkit.db')
    cursor=conn.cursor()
    cursor.execute('''SELECT * FROM tasks WHERE student_email=? and completed=0''',(email,))
    tasks=cursor.fetchall()
    if tasks:
        print(50*"=")
        print("✅ Following are incomplete Tasks!")
        for task in tasks:
            print(f"ID: {task[0]}, Task: {task[2]}, Deadline: {task[4]}, Completed: {task[3]}")
        print(50*"=")
    else:
        print("❌ No incomplete tasks found.")
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
            return  None,False


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
                print("3. View Tasks")
                print("4. Delete Tasks")
                print("5. Mark Task as Completed")
                print("6. View Completed Tasks")
                print("7. View Incomplete Tasks")
                print("8. Resources")
                print("9. Logout")
                sub_choice = input("Enter your choice: ")
                if sub_choice == '1' or sub_choice.lower() == "view profile":
                    profile(student[0])
                elif sub_choice == '2' or sub_choice.lower() == "schedule tasks":
                    schedule_task(student[0])
                elif sub_choice == '3' or sub_choice.lower() == "view tasks":
                    view_tasks(student[0])
                elif sub_choice == '4' or sub_choice.lower() == "delete tasks":
                    delete_tasks(student[0])
                elif sub_choice == '5' or sub_choice.lower() == "mark task as completed":
                    Completed_tasks(student[0])
                elif sub_choice == '6' or sub_choice.lower() == "view completed tasks":
                    view_completed_tasks(student[0])
                elif sub_choice == '7' or sub_choice.lower() == "view incomplete tasks":
                    view_incomplete_tasks(student[0])
                elif sub_choice == '8' or sub_choice.lower() == "resources":
                    resources()
                elif sub_choice == '9'  or sub_choice.lower() == "logout":
                    print("Logging out...")
                    break

        else:
            continue

    elif choice == '3' or choice.lower() == "exit":
        print("Exiting the Student Toolkit. Goodbye!")
        sys.exit()
    else:
        print("Invalid choice. Please try again.")