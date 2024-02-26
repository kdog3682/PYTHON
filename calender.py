from utils import *
from datetime import datetime, timedelta
days_list = [
    'sunday',
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
]
days_map = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6
}


def get_current_season():
    date = datetime.now()
    year = date.year
    spring = datetime(year, 3, 20)
    summer = datetime(year, 6, 21)
    fall = datetime(year, 9, 22)
    winter = datetime(year, 12, 21)

    if spring <= date < summer:
        return 'Spring'
    elif summer <= date < fall:
        return 'Summer'
    elif fall <= date < winter:
        return 'Fall'
    else:
        return 'Winter'



def iso8601(dt):
    return dt.strftime('%Y-%m-%d')


def get_week_range():
    today = datetime.now()
    last_monday = today - timedelta(days=(today.weekday()))
    next_sunday = last_monday + timedelta(days=6)

    store = []
    while last_monday <= next_sunday:
        store.append(last_monday)
        last_monday += timedelta(days=1)
    return store

# datetimes = get_week_range()
# pprint(map(datetimes, iso8601))

def get_next_mondays(day_of_week, n=10):
    # day_of_week: str or int (monday, tuesday, et cetera)
    # Get today's date

    day_of_week = days_map.get(day_of_week, day_of_week)
    today = datetime.now()

    # Calculate the next specified day of the week
    days_until_next_day = (day_of_week - today.weekday() + 7) % 7
    if days_until_next_day == 0:
        days_until_next_day = 7
    next_day = today + timedelta(days=days_until_next_day)

    # Generate a list of the next n occurrences of the specified day
    days = [next_day]
    for _ in range(1, n):
        next_day += timedelta(days=7)
        days.append(next_day)

    return days

# next_50_days = get_next_mondays("sunday", 5)

def get_current_week_number():
    # Get today's date
    today = datetime.now()

    # Get the ISO week number
    week_number = today.isocalendar()[1]
    return week_number

def get_typ_weekly_checklist_data():
    datestamp = iso8601(datetime.now())
    week_number = get_current_week_number()
    user = "Kevin Lee"

    title = f"{datestamp} (Week {week_number})"
    footer = f"{user} Daily Schedule"

    data = {
        "title": title,
        "footer": footer,
        "cells": cells,
        "attrs": attrs,
    }
    return data

pprint(get_typ_weekly_checklist_data())
