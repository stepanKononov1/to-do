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
    );"""

    cursor.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS Projects (
    ProjectID integer,
    Description text,
    Deadline date,
    Created timestamp,
    Completed timestamp,
    PRIMARY KEY(ProjectID)
    );"""
    cursor.execute(sql)
    connection.close()


db = Database()
