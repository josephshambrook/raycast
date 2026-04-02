#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Count Weekdays
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 📅
# @raycast.description Count how many times a weekday appears in a month. E.g. "saturdays this month" or "fridays in august 2027".
# @raycast.packageName Personal
# @raycast.argument1 { "type": "text", "placeholder": "e.g. saturdays this month" }

import sys
import calendar
from datetime import datetime

DAYS = {
    "monday": 0, "mondays": 0,
    "tuesday": 1, "tuesdays": 1,
    "wednesday": 2, "wednesdays": 2,
    "thursday": 3, "thursdays": 3,
    "friday": 4, "fridays": 4,
    "saturday": 5, "saturdays": 5,
    "sunday": 6, "sundays": 6,
}

MONTHS = {
    "january": 1, "jan": 1,
    "february": 2, "feb": 2,
    "march": 3, "mar": 3,
    "april": 4, "apr": 4,
    "may": 5,
    "june": 6, "jun": 6,
    "july": 7, "jul": 7,
    "august": 8, "aug": 8,
    "september": 9, "sep": 9, "sept": 9,
    "october": 10, "oct": 10,
    "november": 11, "nov": 11,
    "december": 12, "dec": 12,
}

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]


def parse_query(query):
    words = query.lower().split()
    now = datetime.now()

    target_day = None
    for word in words:
        if word in DAYS:
            target_day = DAYS[word]
            break

    if target_day is None:
        return None, None, None

    target_month = now.month
    target_year = now.year

    if "next" in words and "month" in words:
        if now.month == 12:
            target_month, target_year = 1, now.year + 1
        else:
            target_month = now.month + 1
    elif "last" in words and "month" in words:
        if now.month == 1:
            target_month, target_year = 12, now.year - 1
        else:
            target_month = now.month - 1
    else:
        for word in words:
            if word in MONTHS:
                target_month = MONTHS[word]
                break
        for word in words:
            if word.isdigit() and len(word) == 4:
                target_year = int(word)
                break

    return target_day, target_month, target_year


def count_weekday(weekday, month, year):
    # calendar.monthcalendar uses Mon=0 .. Sun=6, matching Python's weekday()
    return sum(1 for week in calendar.monthcalendar(year, month) if week[weekday] != 0)


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print("Usage: 'saturdays this month' or 'fridays in august 2027'")
        sys.exit(1)

    query = sys.argv[1].strip()
    target_day, target_month, target_year = parse_query(query)

    if target_day is None:
        print("Couldn't find a day name. Try: 'saturdays this month'")
        sys.exit(1)

    count = count_weekday(target_day, target_month, target_year)
    day_name = DAY_NAMES[target_day]
    month_name = MONTH_NAMES[target_month - 1]

    print(f"{count} {day_name}s in {month_name} {target_year}")


if __name__ == "__main__":
    main()
