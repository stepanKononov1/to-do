import datetime
from db_controller import DbController


def split_delta_time_to_weeks(deadline_start: datetime.datetime, deadline_end: datetime.datetime) -> list:
    start = deadline_start
    weeks = []
    while start < deadline_end:
        start += datetime.timedelta(days=7)
        weeks.append(start)
    return weeks


class Sorter:
    def __init__(self, dbname: str):
        self.dbname = dbname
        self.sort_data()

    def sort_data(self):
        db = DbController(self.dbname)
        subjects = db.get_all_subjects()
        date_starts = db.get_all_date_starts()
        deadlines = db.get_all_deadlines()
        date_starts.sort()
        deadlines.sort()
        state = db.get_state()
        if state:
            deadlines = []
        for deadline, date_start in zip(deadlines, date_starts):
            req_subjects = [subject for subject in subjects if subject[1] == deadline]
            if not req_subjects:
                continue
            periods = split_delta_time_to_weeks(date_start, deadline)
            weeks_total = len(periods)
            period_topics = []
            for subject in req_subjects:
                subject_name = subject[0]
                topics = db.get_topics(subject_name)
                topics_total = len(topics)
                topics_abs_float = round(topics_total / weeks_total, 1)
                topics_density = int(topics_abs_float)
                topics_exception = int(1 / (topics_abs_float % 1))
                for period in periods:
                    count = periods.index(period)
                    if count % topics_exception == 0:
                        try:
                            topic = topics.pop(0)
                            period_topics.append([period.date(), *topic])
                        except IndexError:
                            break
                    for _ in range(topics_density):
                        try:
                            topic = topics.pop(0)
                            period_topics.append([period.date(), *topic])
                        except IndexError:
                            break
            for period in periods:
                total_hours = 0
                for period_topic in period_topics:
                    deadline, max_hours = period_topic[0], period_topic[3]
                    if deadline == period.date():
                        total_hours += max_hours
            period_topics.sort(key=lambda x: x[0])
            [db.add_task(description=f'{period[1]}: {period[2]}', deadline=period[0])
             for period in period_topics]


sorter = Sorter('to_do.db')
