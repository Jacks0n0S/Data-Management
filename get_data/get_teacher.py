from tkinter import simpledialog, messagebox
from database import connect_db

def on_get_teachers():
    class_name = simpledialog.askstring("Ввод", "Введите название класса:")
    
    if not class_name:
        messagebox.showerror("Ошибка", "Пожалуйста, введите название класса.")
        return
    
    class_id = get_class_id(class_name)
    if not class_id:
        messagebox.showerror("Ошибка", f"Класс {class_name} не найден.")
        return
    
    teachers = get_teachers_for_class(class_id)
    
    if teachers:
        teacher_names = "\n".join([f"{teacher[0]} {teacher[1]}" for teacher in teachers])
        messagebox.showinfo("Учителя класса", f"Учителя, преподающие в классе {class_name}:\n\n{teacher_names}")
    else:
        messagebox.showinfo("Учителя класса", f"В классе {class_name} нет преподавателей.")

def get_class_id(class_name):
    query = '''SELECT id FROM classes WHERE name = ?;'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (class_name,))
    class_id = cursor.fetchone()
    connection.close()
    return class_id[0] if class_id else None

def get_teachers_for_class(class_id):
    query = '''
        SELECT teachers.first_name, teachers.last_name
        FROM teachers
        JOIN teacher_subjects ON teachers.id = teacher_subjects.teacher_id
        JOIN lessons ON teacher_subjects.subject_id = lessons.subject_id
        WHERE lessons.class_id = ?;
    '''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (class_id,))
    teachers = cursor.fetchall()
    connection.close()
    return teachers
