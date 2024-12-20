from tkinter import simpledialog, messagebox
from database import connect_db
import sqlite3

def on_add_teacher():
    first_name = simpledialog.askstring("Ввод", "Введите имя учителя:")
    last_name = simpledialog.askstring("Ввод", "Введите фамилию учителя:")
    room_number = simpledialog.askstring("Ввод", "Введите номер кабинета (оставьте пустым, если не требуется):")
    
    if not first_name or not last_name:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните имя и фамилию учителя.")
        return
    
    teacher_id = add_teacher(first_name, last_name, room_number)
    
    if teacher_id:
        subjects = simpledialog.askstring("Ввод", "Введите предметы, которые преподает учитель, через запятую:")
        
        if subjects:
            subject_list = subjects.split(',')
            for subject in subject_list:
                subject = subject.strip()
                subject_id = get_subject_id(subject)
                if not subject_id:
                    add_new = messagebox.askyesno("Предмет не найден", f"Предмет '{subject}' не найден. Хотите добавить его?")
                    if add_new:
                        add_subject(subject)

        else:
            messagebox.showwarning("Предупреждение", "Учитель не имеет предметов.")
        
        messagebox.showinfo("Успех", "Учитель добавлен!")
    else:
        messagebox.showerror("Ошибка", "Не удалось добавить учителя.")

def add_teacher(first_name, last_name, room_number):
    query = '''
            INSERT INTO teachers (first_name, last_name, room_number)
            VALUES (?, ?, ?);
            '''
    params = (first_name, last_name, room_number if room_number else None)
    return execute_modify_query(query, params)

def get_subject_id(subject_name):
    query = '''
            SELECT id FROM subjects WHERE name = ?;
            '''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (subject_name,))
    subject_id = cursor.fetchone()
    connection.close()
    return subject_id[0] if subject_id else None

def link_teacher_to_subject(teacher_id, subject_id):
    query = '''SELECT 1 FROM teacher_subjects WHERE teacher_id = ? AND subject_id = ?'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (teacher_id, subject_id))
    if cursor.fetchone():
        return  
    
    query = '''
            INSERT INTO teacher_subjects (teacher_id, subject_id)
            VALUES (?, ?);
            '''
    params = (teacher_id, subject_id)
    execute_modify_query(query, params)


def execute_modify_query(query, params=()):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        if query.startswith('INSERT'):
            return cursor.lastrowid 
        return cursor.rowcount
    except sqlite3.Error as e:
        connection.rollback()
        print(f"Ошибка при выполнении запроса: {e}")
        return 0
    finally:
        connection.close()

def add_subject(subject_name):
    query = '''
            INSERT INTO subjects (name)
            VALUES (?);
            '''
    execute_modify_query(query, (subject_name,))
    messagebox.showinfo("Успех", f"Предмет '{subject_name}' добавлен в базу данных.")

