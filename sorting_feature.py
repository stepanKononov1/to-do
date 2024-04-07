import datetime
from db_controller import DbController


def split_delta_time_to_weeks(deadline_start: datetime.datetime, deadline_end: datetime.datetime) -> list:
    start = deadline_start
    weeks = []
    while start < deadline_end:
        start += datetime.timedelta(days=7)
        weeks.append(start)
    return weeks


db = DbController('to_do.db')
date_start = datetime.date(datetime.datetime.now().year, 9, 1)
date_start = datetime.datetime.combine(date_start, datetime.datetime.min.time())
subjects = db.get_all_subjects()
deadlines = db.get_all_deadlines()
deadlines.sort()
for deadline in deadlines:
    req_subjects = [subject for subject in subjects if subject[1] == deadline]
    if req_subjects is None:
        continue
    try:
        semester = req_subjects[0][2]
    except IndexError:
        continue
    difference_seconds = (deadline - date_start).total_seconds()
    difference_hours = int(difference_seconds / 3600)
    periods = split_delta_time_to_weeks(date_start, deadline)
    weeks_total = len(periods)
    load = db.get_all_sum_hours_semester(semester)
    avg_load_per_period = int(load / weeks_total) + 1
    print(avg_load_per_period, ' avg')
    period_topics = []
    for subject in req_subjects:
        subject_name = subject[0]
        topics = db.get_topics(subject_name)
        topics_total = len(topics)
        topics_density = int(topics_total / weeks_total) + 1
        for period in periods:
            for _ in range(topics_density):
                try:
                    topic = topics.pop()
                    period_topics.append([period, *topic])
                except IndexError:
                    break
    for period in periods:
        total_hours = 0
        for period_topic in period_topics:
            deadline, max_hours = period_topic[0], period_topic[3]
            if deadline == period:
                total_hours += max_hours
        print(total_hours)
    date_start = deadline
