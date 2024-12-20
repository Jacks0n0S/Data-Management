import sqlite3
import bcrypt
import tkinter as tk
from tkinter import messagebox
from my_import import *

def add_user(username, password, role):
    conn = sqlite3.connect('SchoolDB.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    if cursor.fetchone():
        return

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute('''INSERT INTO Users (username, password, role) 
                      VALUES (?, ?, ?)''', (username, hashed_password, role))

    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect('SchoolDB.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        stored_password = user[2]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return user 
    return None

def login_window():
    login_win = tk.Tk()
    login_win.title("Вход")

    tk.Label(login_win, text="Имя пользователя:").pack(padx=10, pady=5)
    username_entry = tk.Entry(login_win)
    username_entry.pack(padx=10, pady=5)

    tk.Label(login_win, text="Пароль:").pack(padx=10, pady=5)
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack(padx=10, pady=5)

    def on_login():
        username = username_entry.get()
        password = password_entry.get()

        user = authenticate_user(username, password)
        if user:
            messagebox.showinfo("Успех", f"Добро пожаловать, {user[1]}!")
            login_win.destroy()

            show_main_window(user)
        else:
            messagebox.showerror("Ошибка", "Неверные имя пользователя или пароль")

    tk.Button(login_win, text="Войти", command=on_login).pack(padx=10, pady=5)
    login_win.mainloop()

def show_main_window(user):
    role = user[3]
    root = tk.Tk()
    root.title("Школа")

    if role == 'admin':
        btn_get_lesson = tk.Button(root, text="Какой предмет будет в заданном классе?", command=on_get_subject)
        btn_get_lesson.pack(fill=tk.X, padx=10, pady=5)

        btn_get_teacher = tk.Button(root, text="Кто из учителей преподает в заданном классе?", command=on_get_teachers)
        btn_get_teacher.pack(fill=tk.X, padx=10, pady=5)

        btn_get_classroom = tk.Button(root, text="В каком кабинете будет n-й урок?", command=on_get_room)
        btn_get_classroom.pack(fill=tk.X, padx=10, pady=5)

        btn_get_classes = tk.Button(root, text="В каких классах преподает учитель заданный предмет?", command=on_get_classes)
        btn_get_classes.pack(fill=tk.X, padx=10, pady=5)

        btn_get_timetable = tk.Button(root, text="Расписание на заданный день недели для класса.", command=on_get_timetable)
        btn_get_timetable.pack(fill=tk.X, padx=10, pady=5)

        btn_set_teacher = tk.Button(root, text="Внести информацию о новом учителе", command=on_add_teacher)
        btn_set_teacher.pack(fill=tk.X, padx=10, pady=5)

        btn_delete_student = tk.Button(root, text="Удалить запись об ученике", command=on_delete_student)
        btn_delete_student.pack(fill=tk.X, padx=10, pady=5)

        btn_change_grade = tk.Button(root, text="Изменить оценку ученику", command=on_add_grade)
        btn_change_grade.pack(fill=tk.X, padx=10, pady=5)

        btn_get_reference = tk.Button(root, text="Получить справку о количестве учеников в заданном классе", command=on_get_student_count)
        btn_get_reference.pack(fill=tk.X, padx=10, pady=5)

        btn_get_report = tk.Button(root, text="Получить отчет о работе школы", command=on_generate_school_report)
        btn_get_report.pack(fill=tk.X, padx=10, pady=5)

    elif role == 'user':
        btn_get_lesson = tk.Button(root, text="Какой предмет будет в заданном классе?", command=on_get_subject)
        btn_get_lesson.pack(fill=tk.X, padx=10, pady=5)

        btn_get_teacher = tk.Button(root, text="Кто из учителей преподает в заданном классе?", command=on_get_teachers)
        btn_get_teacher.pack(fill=tk.X, padx=10, pady=5)

        btn_get_classroom = tk.Button(root, text="В каком кабинете будет n-й урок?", command=on_get_room)
        btn_get_classroom.pack(fill=tk.X, padx=10, pady=5)

        btn_get_classes = tk.Button(root, text="В каких классах преподает учитель заданный предмет?", command=on_get_classes)
        btn_get_classes.pack(fill=tk.X, padx=10, pady=5)

        btn_get_timetable = tk.Button(root, text="Расписание на заданный день недели для класса.", command=on_get_timetable)
        btn_get_timetable.pack(fill=tk.X, padx=10, pady=5)

        btn_change_grade = tk.Button(root, text="Изменить оценку ученику", command=on_add_grade)
        btn_change_grade.pack(fill=tk.X, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_tables()
    #add_user("director", "123", "admin")
    #add_user("teacher", "123", "user")
    login_window()
