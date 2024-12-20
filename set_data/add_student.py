from tkinter import simpledialog, messagebox
from database import connect_db
import sqlite3

def on_add_student():
    first_name = simpledialog.askstring("Ввод", "Введите имя ученика:")
    last_name = simpledialog.askstring("Ввод", "Введите фамилию ученика:")
    class_name = simpledialog.askstring("Ввод", "Введите класс ученика:")

    if not first_name or not last_name or not class_name:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
        return
    
    class_id = get_class_id(class_name)
    if not class_id:
        class_id = add_class(class_name)
        create_schedule_for_class(class_id)

    student_id = add_student(first_name, last_name, class_id)
    
    if student_id:
        messagebox.showinfo("Успех", "Ученик добавлен!")
    else:
        messagebox.showerror("Ошибка", "Не удалось добавить ученика.")

def get_class_id(class_name):
    query = '''SELECT id FROM classes WHERE name = ?;'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (class_name,))
    class_id = cursor.fetchone()
    connection.close()
    return class_id[0] if class_id else None

def add_class(class_name):
    query = '''INSERT INTO classes (name) VALUES (?);'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (class_name,))
    connection.commit()
    class_id = cursor.lastrowid
    connection.close()
    return class_id

def add_student(first_name, last_name, class_id):
    query = '''INSERT INTO students (first_name, last_name, class_id) VALUES (?, ?, ?);'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (first_name, last_name, class_id))
    connection.commit()
    student_id = cursor.lastrowid
    connection.close()
    return student_id

def create_schedule_for_class(class_id):
    days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
    
    while True:
        subject_name = simpledialog.askstring("Ввод", "Введите название предмета (или оставьте пустым, чтобы закончить):")
        if not subject_name:
            break
        
        subject_id = get_subject_id(subject_name)
        if not subject_id:
            subject_id = add_subject(subject_name)
        
        day_of_week = simpledialog.askstring("Ввод", f"Введите день недели для предмета '{subject_name}' из списка {', '.join(days_of_week)}:")
        if day_of_week not in days_of_week:
            messagebox.showerror("Ошибка", "Неверный день недели.")
            return

        teacher_first_name = simpledialog.askstring("Ввод", f"Введите имя учителя для предмета '{subject_name}':")
        teacher_last_name = simpledialog.askstring("Ввод", f"Введите фамилию учителя для предмета '{subject_name}':")
        teacher_room = simpledialog.askstring("Ввод", "Введите номер кабинета учителя:")
        
        teacher_id = add_teacher(teacher_first_name, teacher_last_name, teacher_room)

        link_teacher_to_subject(teacher_id, subject_id)
        
        add_lesson(class_id, subject_id, teacher_id, day_of_week)

def get_subject_id(subject_name):
    query = '''SELECT id FROM subjects WHERE name = ?;'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (subject_name,))
    subject_id = cursor.fetchone()
    connection.close()
    return subject_id[0] if subject_id else None

def add_subject(subject_name):
    query = '''INSERT INTO subjects (name) VALUES (?);'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (subject_name,))
    connection.commit()
    subject_id = cursor.lastrowid
    connection.close()
    return subject_id

def add_teacher(first_name, last_name, room_number):
    query = '''INSERT INTO teachers (first_name, last_name, room_number) VALUES (?, ?, ?);'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (first_name, last_name, room_number))
    connection.commit()
    teacher_id = cursor.lastrowid
    connection.close()
    return teacher_id

def link_teacher_to_subject(teacher_id, subject_id):
    query = '''INSERT INTO teacher_subjects (teacher_id, subject_id) VALUES (?, ?);'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (teacher_id, subject_id))
    connection.commit()
    connection.close()

def add_lesson(class_id, subject_id, teacher_id, day_of_week):
    lesson_number = simpledialog.askinteger("Ввод", f"Введите номер урока для предмета в день {day_of_week}:")
    room_number = simpledialog.askstring("Ввод", "Введите номер кабинета для урока:")
    
    query = '''INSERT INTO lessons (class_id, subject_id, teacher_id, day_of_week, lesson_number, room_number)
               VALUES (?, ?, ?, ?, ?, ?);'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (class_id, subject_id, teacher_id, day_of_week, lesson_number, room_number))
    connection.commit()
    connection.close()


