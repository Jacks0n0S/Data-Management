from tkinter import simpledialog, messagebox
from database import connect_db
import sqlite3


def on_get_subject():
    class_name = simpledialog.askstring("Запрос", "Введите класс (например, 5А):")
    day_of_week = simpledialog.askstring(
        "Запрос", "Введите день недели (например, Понедельник):"
    )
    lesson_number = simpledialog.askinteger(
        "Запрос", "Введите номер урока (например, 2):"
    )
    
    if not (class_name and day_of_week and lesson_number):
        messagebox.showerror("Ошибка", "Все поля обязательны для заполнения.")
        return

    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM classes WHERE name = ?", (class_name,))
        class_id = cursor.fetchone()
        if not class_id:
            messagebox.showwarning("Предупреждение", f"Класс '{class_name}' не найден.")
            return
        class_id = class_id[0]

        query = '''
            SELECT s.name 
            FROM lessons l
            JOIN subjects s ON l.subject_id = s.id
            WHERE l.class_id = ? AND l.day_of_week = ? AND l.lesson_number = ?
        '''
        cursor.execute(query, (class_id, day_of_week, lesson_number))
        subject = cursor.fetchone()

        if subject:
            messagebox.showinfo("Результат", f"Предмет на {lesson_number}-м уроке в {day_of_week} для класса {class_name}: {subject[0]}.")
        else:
            messagebox.showinfo("Результат", f"На {lesson_number}-м уроке в {day_of_week} для класса {class_name} предмет не найден.")
    
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
    finally:
        connection.close()
