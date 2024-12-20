from tkinter import simpledialog, messagebox
from database import connect_db

def on_get_classes():
    teacher_name = simpledialog.askstring("Ввод", "Введите имя учителя:")
    subject_name = simpledialog.askstring("Ввод", "Введите название предмета:")
    
    if not teacher_name or not subject_name:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
        return
    
    teacher_id = get_teacher_id(teacher_name)
    if not teacher_id:
        messagebox.showerror("Ошибка", f"Учитель {teacher_name} не найден.")
        return
    
    subject_id = get_subject_id(subject_name)
    if not subject_id:
        messagebox.showerror("Ошибка", f"Предмет {subject_name} не найден.")
        return
    
    classes = get_classes_for_teacher_and_subject(teacher_id, subject_id)
    
    if classes:
        class_names = ', '.join(classes)
        messagebox.showinfo("Классы", f"Учитель {teacher_name} преподает {subject_name} в следующих классах: {class_names}")
    else:
        messagebox.showinfo("Классы", f"Учитель {teacher_name} не преподает {subject_name} в любом классе.")

def get_teacher_id(teacher_name):
    first_name, last_name = teacher_name.split()
    
    query = '''SELECT id FROM teachers WHERE first_name = ? AND last_name = ?;'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (first_name, last_name))
    teacher_id = cursor.fetchone()
    connection.close()
    return teacher_id[0] if teacher_id else None

def get_subject_id(subject_name):
    query = '''SELECT id FROM subjects WHERE name = ?;'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (subject_name,))
    subject_id = cursor.fetchone()
    connection.close()
    return subject_id[0] if subject_id else None

def get_classes_for_teacher_and_subject(teacher_id, subject_id):
    query = '''
        SELECT c.name
        FROM lessons l
        JOIN classes c ON l.class_id = c.id
        WHERE l.teacher_id = ? AND l.subject_id = ?;
    '''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (teacher_id, subject_id))
    classes = cursor.fetchall()
    connection.close()
    return [class_[0] for class_ in classes] 

def check_class_exists(class_name):
    query = '''SELECT id FROM classes WHERE name = ?;'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (class_name,))
    class_id = cursor.fetchone()
    connection.close()
    return class_id is not None

def check_teacher_exists(teacher_name):
    first_name, last_name = teacher_name.split()
    query = '''SELECT id FROM teachers WHERE first_name = ? AND last_name = ?;'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (first_name, last_name))
    teacher_id = cursor.fetchone()
    connection.close()
    return teacher_id is not None

def add_student_and_schedule():
    student_name = simpledialog.askstring("Ввод", "Введите имя ученика:")
    class_name = simpledialog.askstring("Ввод", "Введите класс ученика:")
    
    if not student_name or not class_name:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
        return
    
    if not check_class_exists(class_name):
        messagebox.showerror("Ошибка", f"Класс {class_name} не найден.")
        return
    
    if not check_teacher_exists(student_name):
        messagebox.showerror("Ошибка", f"Ученик {student_name} не найден.")
        return
    
    messagebox.showinfo("Успех", f"Ученик {student_name} успешно добавлен в класс {class_name}.")

