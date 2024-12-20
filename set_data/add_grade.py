from tkinter import simpledialog, messagebox
from database import connect_db
import sqlite3


def on_add_grade():
    first_name = simpledialog.askstring("Изменение оценки", "Введите имя ученика:")
    last_name = simpledialog.askstring("Изменение оценки", "Введите фамилию ученика:")
    class_name = simpledialog.askstring("Изменение оценки", "Введите класс ученика:")
    subject_name = simpledialog.askstring("Изменение оценки", "Введите предмет:")
    new_grade = simpledialog.askinteger("Изменение оценки", "Введите новую оценку (1-5):")
    
    if not (first_name and last_name and class_name and subject_name and new_grade):
        messagebox.showerror("Ошибка", "Все поля обязательны для заполнения.")
        return

    if new_grade < 1 or new_grade > 5:
        messagebox.showerror("Ошибка", "Оценка должна быть в диапазоне от 1 до 5.")
        return

    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM classes WHERE name = ?", (class_name,))
        class_id = cursor.fetchone()
        if not class_id:
            cursor.execute("INSERT INTO classes (name) VALUES (?)", (class_name,))
            class_id = cursor.lastrowid
        else:
            class_id = class_id[0]

        cursor.execute(
            "SELECT id FROM students WHERE first_name = ? AND last_name = ? AND class_id = ?",
            (first_name, last_name, class_id),
        )
        student_id = cursor.fetchone()
        if not student_id:
            cursor.execute(
                "INSERT INTO students (first_name, last_name, class_id) VALUES (?, ?, ?)",
                (first_name, last_name, class_id),
            )
            student_id = cursor.lastrowid
        else:
            student_id = student_id[0]

        cursor.execute("SELECT id FROM subjects WHERE name = ?", (subject_name,))
        subject_id = cursor.fetchone()
        if not subject_id:
            cursor.execute("INSERT INTO subjects (name) VALUES (?)", (subject_name,))
            subject_id = cursor.lastrowid
        else:
            subject_id = subject_id[0]

        cursor.execute(
            "SELECT id FROM grades WHERE student_id = ? AND subject_id = ?",
            (student_id, subject_id),
        )
        grade_id = cursor.fetchone()
        if not grade_id:
            cursor.execute(
                "INSERT INTO grades (student_id, subject_id, grade) VALUES (?, ?, ?)",
                (student_id, subject_id, new_grade),
            )
            messagebox.showinfo("Успех", "Оценка добавлена.")
        else:
            cursor.execute(
                "UPDATE grades SET grade = ? WHERE id = ?", (new_grade, grade_id[0])
            )
            messagebox.showinfo("Успех", "Оценка обновлена.")

        connection.commit()

    except sqlite3.Error as e:
        connection.rollback()
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
    finally:
        connection.close()
