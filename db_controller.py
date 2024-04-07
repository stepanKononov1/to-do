import sqlite3
import datetime


class DbController:
    """Allows user to update task and projects in database"""

    def __init__(self, db_name):
        self.db_name = db_name

    def query(self, sql, data):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute(sql, data)
            db.commit()

    def select_query(self, sql, data=None):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)
            results = cursor.fetchall()
        return results

    def add_task(self, description, deadline):
        created = datetime.datetime.now()
        sql_add_task = "INSERT INTO Tasks (Description, Deadline, Created) VALUES (?,?,?)"
        self.query(sql_add_task, (description, deadline, created))

    def delete_task(self, task_id):
        self.query("DELETE FROM Tasks WHERE TaskID = ?", (task_id,))

    def mark_task_completed(self, task_id):
        completed = datetime.datetime.now()
        sql_mark_completed = "UPDATE Tasks SET Completed = ? WHERE TaskID = ?"
        self.query(sql_mark_completed, (completed, task_id))

    def edit_task_description(self, task_id, description):
        sql_edit_descr = "UPDATE Tasks SET Description = ? WHERE TaskID = ?"
        self.query(sql_edit_descr, (description, task_id))

    def set_task_deadline(self, task_id, deadline):
        sql_set_deadline = "UPDATE Tasks SET Deadline = ? WHERE TaskID = ?"
        self.query(sql_set_deadline, (deadline, task_id))

    def get_all_tasks(self):
        results = self.select_query("SELECT * FROM Tasks")
        return results

    def get_active_tasks(self):
        results = self.select_query("SELECT * FROM Tasks WHERE Completed IS NULL")
        return results

    def get_completed_tasks(self):
        results = self.select_query("SELECT * FROM Tasks WHERE Completed IS NOT NULL")
        return results

    def get_single_task(self, task_id):
        results = self.select_query("SELECT * FROM Tasks WHERE TaskID = ?", (task_id,))
        return results

    def get_sum_hours_subject(self, subject, semester):
        try:
            results = self.select_query("SELECT sum(hours) FROM Edu_subjects WHERE subject = ? AND semester = ?",
                                        (subject, semester,))
            return results
        except:
            return

    def get_all_sum_hours_semester(self, semester):
        try:
            sql = """
            SELECT sum(max_hours) FROM _Topics WHERE (SELECT semester FROM _Subjects) = ?
            """
            results = self.select_query(sql, [semester,])
            return results[0][0]
        except:
            return

    def get_all_subjects(self):
        sql = """
        SELECT subject_name_uniq,
        (SELECT deadline FROM _Semesters WHERE _Subjects.semester = _Semesters.semester) as deadline,
        semester
        FROM _Subjects
        """
        try:
            results = self.select_query(sql)
            results = [(subject[0],
                        datetime.datetime.strptime(subject[1], '%d.%m.%Y'),
                        subject[2]) for subject in results]
            return results
        except:
            return

    def get_all_deadlines(self):
        sql = """
        SELECT deadline
        FROM _Semesters
        """
        try:
            results = [x[0] for x in self.select_query(sql)]
            results = [datetime.datetime.strptime(subject, '%d.%m.%Y') for subject in results]
            return results
        except:
            return

    def get_topics(self, topic_subject):
        sql = """
        SELECT topic_subject, topic_name, max_hours
        FROM _Topics
        WHERE topic_subject = ?
        """
        try:
            results = self.select_query(sql=sql, data=[topic_subject,])
            return results
        except:
            return
