import sqlite3


class Database:
    connection = sqlite3.connect("to_do.db")
    cursor = connection.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS Tasks (
    TaskID integer,
    Description text,
    Deadline date,
    Created timestamp,
    Completed timestamp,
    ProjectID integer,
    PRIMARY KEY(TaskID),
    FOREIGN KEY(ProjectID) REFERENCES Projects(ProjectID)
    );
    CREATE TABLE IF NOT EXISTS Edu_deadlines (
    pk INTEGER NOT NULL UNIQUE,
    course INTEGER,
    semester INTEGER,
    IC_semester_deadline TEXT,
    PRIMARY KEY (pk AUTOINCREMENT)
    );
    CREATE TABLE IF NOT EXISTS Edu_semester_data (
    id INTEGER NOT NULL UNIQUE,
    Edu_deadline_pk	INTEGER,
    subject	TEXT,
    max_hours INTEGER,
    PRIMARY KEY(id AUTOINCREMENT)
    );
    CREATE TABLE Edu_subjects (
    pk INTEGER,
    subject TEXT,
    topic TEXT UNIQUE,
    hours INTEGER,
    PRIMARY KEY(pk AUTOINCREMENT)
    );
    """
    connection.close()


db = Database()

