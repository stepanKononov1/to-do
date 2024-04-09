import sqlite3
import csv
import db_controller


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
    PRIMARY KEY(TaskID)
    );
    """
    cursor.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS "_Semesters" (
    "semester"	INTEGER,
    "course"	INTEGER,
    "start"	    TEXT,
    "deadline"	TEXT,
    PRIMARY KEY("semester")
    )
    """
    cursor.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS "_Subjects" (
    "subject_name_uniq"	TEXT,
    "semester"
    INTEGER
    CHECK((semester > 0 and semester < 9000)),
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
    tables = ['_Topics', '_Subjects', '_Semesters']
    for table in tables:
        sql = """SELECT * FROM Tasks"""
        result = cursor.execute(sql).fetchall()
        if result:
            break
        sql = f"""SELECT * FROM {table}"""
        result = cursor.execute(sql).fetchall()
        if result:
            cursor.execute(f'DELETE FROM {table}')
            connection.commit()
        try:
            with open(f'{table}.csv', 'r', encoding='utf-8') as f_open_csv:
                rows = csv.reader(f_open_csv, delimiter=",")
                for row in rows:
                    values = '?'
                    for _ in row:
                        values += ',?'
                    values = values.rsplit(',?', 1)[0]
                    try:
                        cursor.execute(f'INSERT INTO {table} VALUES ({values})', row)
                        connection.commit()
                    except sqlite3.IntegrityError:
                        continue
        except FileNotFoundError:
            continue

    connection.close()


db = Database()

