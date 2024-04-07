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
    ProjectID text,
    PRIMARY KEY(TaskID)
    );
    """
    cursor.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS "_Semesters" (
    "semester"	INTEGER,
    "course"	INTEGER,
    "deadline"	TEXT,
    PRIMARY KEY("semester")
    )
    """
    cursor.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS "_Subjects" (
    "subject_name_uniq"	TEXT,
    "semester"	INTEGER,
    PRIMARY KEY("subject_name_uniq")
    )
    """
    cursor.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS "_Topics" (
    "pk"	INTEGER,
    "topic_subject"	TEXT,
    "topic_name"	TEXT,
    "max_hours"	INTEGER,
    PRIMARY KEY("pk")
    )
    """
    cursor.execute(sql)
    connection.close()


db = Database()

