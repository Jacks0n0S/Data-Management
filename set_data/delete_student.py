from tkinter import simpledialog, messagebox
import sqlite3
from database import connect_db

def on_delete_student():
    first_name = simpledialog.askstring("Удаление ученика", "Введите имя ученика:")
    last_name = simpledialog.askstring("Удаление ученика", "Введите фамилию ученика:")
    class_name = simpledialog.askstring("Удаление ученика", "Введите класс ученика (опционально):")
    
    if not first_name or not last_name:
        messagebox.showerror("Ошибка", "Имя и фамилия ученика обязательны для удаления.")
        return

    try:
        connection = connect_db()
        cursor = connection.cursor()

        if class_name:
            query = '''
                    SELECT s.id FROM students s
                    JOIN classes c ON s.class_id = c.id
                    WHERE s.first_name = ? AND s.last_name = ? AND c.name = ?
                    '''
            cursor.execute(query, (first_name, last_name, class_name))
        else:
            query = '''
                    SELECT id FROM students
                    WHERE first_name = ? AND last_name = ?
                    '''
            cursor.execute(query, (first_name, last_name))

        student_ids = [row[0] for row in cursor.fetchall()]

        if not student_ids:
            messagebox.showwarning("Предупреждение", "Ученик с указанными данными не найден.")
            return

        cursor.executemany("DELETE FROM grades WHERE student_id = ?", [(student_id,) for student_id in student_ids])

        cursor.executemany("DELETE FROM students WHERE id = ?", [(student_id,) for student_id in student_ids])

        connection.commit()
        
        messagebox.showinfo("Успех", f"Удалено {len(student_ids)} учеников и их данные.")
    
    except sqlite3.Error as e:
        connection.rollback()
        messagebox.showerror("Ошибка", f"Произошла ошибка при удалении ученика: {e}")
    finally:
        connection.close()

