from tkinter import simpledialog, messagebox
from database import connect_db

def on_get_timetable():
    class_name = simpledialog.askstring("Ввод", "Введите класс:")
    day_of_week = simpledialog.askstring("Ввод", "Введите день недели:")

    if not class_name or not day_of_week:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
        return
    
    if not check_class_exists(class_name):
        messagebox.showerror("Ошибка", f"Класс {class_name} не найден.")
        return
    
    schedule = get_class_schedule_for_day(class_name, day_of_week)
    
    if schedule:
        schedule_info = "\n".join([f"{lesson[0]}: {lesson[1]} (Учитель: {lesson[2]}, Кабинет: {lesson[3]})" 
                                   for lesson in schedule])
        messagebox.showinfo("Расписание", f"Расписание для класса {class_name} на {day_of_week}:\n\n{schedule_info}")
    else:
        messagebox.showinfo("Расписание", f"Расписание для класса {class_name} на {day_of_week} не найдено.")

def get_class_schedule_for_day(class_name, day_of_week):
    query = '''
        SELECT s.name, l.lesson_number, t.first_name || ' ' || t.last_name AS teacher_name, l.room_number
        FROM lessons l
        JOIN subjects s ON l.subject_id = s.id
        JOIN teachers t ON l.teacher_id = t.id
        JOIN classes c ON l.class_id = c.id
        WHERE c.name = ? AND l.day_of_week = ?
        ORDER BY l.lesson_number;
    '''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (class_name, day_of_week))
    lessons = cursor.fetchall()
    connection.close()
    return lessons

def check_class_exists(class_name):
    query = '''SELECT id FROM classes WHERE name = ?;'''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, (class_name,))
    class_id = cursor.fetchone()
    connection.close()
    return class_id is not None
