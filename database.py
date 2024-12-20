import sqlite3

def connect_db():
    return sqlite3.connect('SchoolDB.db')

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Таблица 'Учителя'
    cursor.execute('''CREATE TABLE IF NOT EXISTS teacher_subjects (
                      teacher_id INTEGER NOT NULL,
                      subject_id INTEGER NOT NULL,
                      FOREIGN KEY(teacher_id) REFERENCES teachers(id),
                      FOREIGN KEY(subject_id) REFERENCES subjects(id),
                      PRIMARY KEY (teacher_id, subject_id)
                 )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS teachers (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      first_name VARCHAR(50) NOT NULL,
                      last_name VARCHAR(70) NOT NULL,
                      room_number INTEGER NULL
                )''')
    
    # Таблица 'Классы'
    cursor.execute('''CREATE TABLE IF NOT EXISTS classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(3) NOT NULL
                  )''')

    # Таблица 'Ученик'
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    class_id INTEGER NOT NULL,
                    FOREIGN KEY(class_id) REFERENCES classes(id)
                  )''')

    # Таблица 'Предметы'
    cursor.execute('''CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL UNIQUE
                  )''')

    # Таблица 'Уроки'
    cursor.execute('''CREATE TABLE IF NOT EXISTS lessons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_id INTEGER NOT NULL,
                    subject_id INTEGER NOT NULL,
                    teacher_id INTEGER NOT NULL,
                    day_of_week VARCHAR(11) NOT NULL,
                    lesson_number INTEGER NOT NULL,
                    room_number VARCHAR(10),
                    FOREIGN KEY(class_id) REFERENCES classes(id),
                    FOREIGN KEY(subject_id) REFERENCES subjects(id),
                    FOREIGN KEY(teacher_id) REFERENCES teachers(id)
                  )''')
    
    # Таблица 'Оценки'
    cursor.execute('''CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    subject_id INTEGER NOT NULL,
                    grade INTEGER NOT NULL,
                    FOREIGN KEY(student_id) REFERENCES students(id),
                    FOREIGN KEY(subject_id) REFERENCES subjects(id)
                  )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'user'))
                  )''')
    
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_class_id ON lessons (class_id)''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_teacher_id ON lessons (teacher_id)''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_student_id ON grades (student_id)''')
    cursor.execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_teacher_subject ON teacher_subjects (teacher_id, subject_id)''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("База данных успешно создана!")
