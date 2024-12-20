from tkinter import simpledialog, messagebox
from database import connect_db

def on_get_student_count():
    class_name = simpledialog.askstring("Ввод", "Введите класс:")
    
    if not class_name:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните название класса.")
        return
    
    if not check_class_exists(class_name):
        messagebox.showerror("Ошибка", f"Класс {class_name} не найден.")
        return
    
    student_count = count_students_in_class(class_name)
    
    messagebox.showinfo("Количество учеников", f"В классе {class_name} всего {student_count} учеников.")

def count_students_in_class(class_name):
    query = '''
        SELECT COUNT(*) FROM students s
        JOIN classes c ON s.class_id = c.id
        WHERE c.name = ?;
    '''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (class_name,))
    student_count = cursor.fetchone()[0]
    connection.close()
    return student_count

def check_class_exists(class_name):
    query = '''SELECT id FROM classes WHERE name = ?;'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (class_name,))
    class_id = cursor.fetchone()
    connection.close()
    return class_id is not None
