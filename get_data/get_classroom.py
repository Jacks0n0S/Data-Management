from tkinter import simpledialog, messagebox
from database import connect_db

def on_get_room():

    class_name = simpledialog.askstring("Ввод", "Введите название класса:")
    day_of_week = simpledialog.askstring("Ввод", "Введите день недели:")
    lesson_number = simpledialog.askinteger("Ввод", "Введите номер урока (1-5):")
    
    if not class_name or not day_of_week or lesson_number is None:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
        return
    

    class_id = get_class_id(class_name)
    if not class_id:
        messagebox.showerror("Ошибка", f"Класс {class_name} не найден.")
        return
    

    room_number = get_room_for_class(class_id, day_of_week, lesson_number)
    
    if room_number:
        messagebox.showinfo("Кабинет", f"В классе {class_name} на {lesson_number}-м уроке в {day_of_week} будет кабинет: {room_number}")
    else:
        messagebox.showinfo("Кабинет", f"Нет информации о {lesson_number}-м уроке в {day_of_week} для класса {class_name}.")

def get_class_id(class_name):
    query = '''SELECT id FROM classes WHERE name = ?;'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (class_name,))
    class_id = cursor.fetchone()
    connection.close()
    return class_id[0] if class_id else None

def get_room_for_class(class_id, day_of_week, lesson_number):
    query = '''
        SELECT room_number
        FROM lessons
        WHERE class_id = ? AND day_of_week = ? AND lesson_number = ?;
    '''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (class_id, day_of_week, lesson_number))
    room_number = cursor.fetchone()
    connection.close()
    return room_number[0] if room_number else None

