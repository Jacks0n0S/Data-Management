import tkinter as tk
from tkinter import messagebox
from database import connect_db

def on_generate_school_report():
    teacher_count_by_subject = get_teacher_count_by_subject()
    
    room_count = get_unique_room_count()
    
    student_count_by_class, student_categories = get_student_count_by_class()

    report = "Отчет о работе школы:\n\n"
    
    report += "Количество учителей по предметам:\n"
    for subject, count in teacher_count_by_subject.items():
        report += f"{subject}: {count} учителей\n"
    
    report += f"\nКоличество кабинетов: {room_count}\n"
    
    report += "\nЧисло учеников в каждом классе:\n"
    for class_name, count in student_count_by_class.items():
        report += f"{class_name}: {count} учеников\n"
    
    report += "\nКоличество учеников по категориям:\n"
    for class_name, categories in student_categories.items():
        report += f"Класс {class_name}:\n"
        for category, count in categories.items():
            report += f"  {category}: {count} учеников\n"

    show_report_window(report)

def show_report_window(report):
    report_window = tk.Toplevel()
    report_window.title("Отчет о работе школы")
    
    text_widget = tk.Text(report_window, wrap=tk.WORD, width=80, height=20)
    text_widget.insert(tk.END, report)
    text_widget.config(state=tk.DISABLED)
    
    scrollbar = tk.Scrollbar(report_window, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    report_window.mainloop()

def get_teacher_count_by_subject():
    query = '''
        SELECT s.name, COUNT(t.id) 
        FROM subjects s
        LEFT JOIN teacher_subjects ts ON s.id = ts.subject_id
        LEFT JOIN teachers t ON ts.teacher_id = t.id
        GROUP BY s.name;
    '''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    
    teacher_count_by_subject = {subject: count for subject, count in data}
    return teacher_count_by_subject

def get_unique_room_count():
    query = '''
        SELECT COUNT(DISTINCT room_number) 
        FROM teachers 
        WHERE room_number IS NOT NULL;
    '''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query)
    room_count = cursor.fetchone()[0]
    connection.close()
    return room_count

def get_student_count_by_class():
    query = '''
        SELECT c.name, COUNT(s.id) 
        FROM students s
        JOIN classes c ON s.class_id = c.id
        GROUP BY c.name;
    '''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    
    student_count_by_class = {class_name: count for class_name, count in data}

    student_categories = get_student_categories()

    return student_count_by_class, student_categories

def get_student_categories():    
    student_categories = {}
    
    query = '''
        SELECT c.name, g.grade
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN classes c ON s.class_id = c.id;
    '''
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()

    for class_name, grade in data:
        if class_name not in student_categories:
            student_categories[class_name] = {'Двоечников': 0, 'Троечников': 0, 'Хорошистов': 0, 'Оличников': 0}

        if grade == 2:
            student_categories[class_name]['Двоечников'] += 1
        elif grade == 3:
            student_categories[class_name]['Троечников'] += 1
        elif grade == 4:
            student_categories[class_name]['Хорошистов'] += 1
        elif grade == 5:
            student_categories[class_name]['Оличников'] += 1

    return student_categories
