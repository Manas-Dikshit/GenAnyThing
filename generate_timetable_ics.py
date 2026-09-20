"""
Weekly Timetable -> ICS Generator
----------------------------------
Generates a .ics calendar file for the date range 20/09/2026 to 17/10/2026
based on a fixed weekly schedule (Mon-Sun).

Usage:
    python generate_timetable.py

Output:
    timetable_20-09-2026_to_17-10-2026_Demo.ics
"""

from datetime import date, datetime, timedelta


# 1. CONFIG: date range

START_DATE = date(2026, 9, 20)   # inclusive
END_DATE   = date(2026, 10, 17)  # inclusive


# 2. WEEKLY SCHEDULE
# Each entry: (start_hour, start_min, end_hour, end_min, "Title", "Location")
# Location is optional - leave "" if not needed.
# Python's date.weekday(): Monday=0 ... Sunday=6


WEEKLY_SCHEDULE = {
    0: [  # MONDAY
        (7, 0, 7, 30, "Wake up & freshen up", ""),
        (7, 30, 8, 0, "Breakfast", ""),
        (8, 0, 9, 0, "Reading / Study", ""),
        (9, 0, 10, 0, "Class / Lecture", "Room A"),
        (10, 0, 11, 0, "Group Discussion", "Room A"),
        (11, 0, 12, 0, "Workshop", "Room B"),
        (12, 0, 13, 0, "Lunch Break", ""),
        (13, 0, 14, 0, "Library Work", ""),
        (14, 0, 15, 0, "Class / Lecture", "Room C"),
        (15, 0, 16, 0, "Seminar", "Room C"),
        (16, 0, 17, 0, "Sports / Outdoor Activity", ""),
        (17, 0, 17, 30, "Snacks Break", ""),
        (17, 30, 19, 0, "Self Study", ""),
        (19, 0, 20, 0, "Project Work", ""),
        (20, 0, 20, 30, "Relaxation / Music", ""),
        (20, 30, 21, 15, "Dinner", ""),
        (21, 15, 22, 0, "Leisure Activity", ""),
        (22, 0, 22, 30, "Wind down", ""),
    ],
    1: [  # TUESDAY
        (7, 0, 7, 30, "Wake up & freshen up", ""),
        (7, 30, 8, 0, "Breakfast", ""),
        (8, 0, 9, 0, "Class / Lecture", "Room B"),
        (9, 0, 12, 0, "Lab Session", "Lab 1"),
        (12, 0, 13, 0, "Lunch Break", ""),
        (13, 0, 14, 0, "Library Work", ""),
        (14, 0, 15, 0, "Class / Lecture", "Room C"),
        (15, 0, 16, 0, "Seminar", "Room C"),
        (16, 0, 17, 0, "Sports / Outdoor Activity", ""),
        (17, 0, 17, 30, "Snacks Break", ""),
        (17, 30, 19, 0, "Self Study", ""),
        (19, 0, 20, 0, "Creative Work", ""),
        (20, 0, 20, 30, "Relaxation", ""),
        (20, 30, 21, 15, "Dinner", ""),
        (21, 15, 22, 0, "Leisure Activity", ""),
        (22, 0, 22, 30, "Wind down", ""),
    ],
    2: [  # WEDNESDAY
        (7, 0, 7, 30, "Wake up & freshen up", ""),
        (7, 30, 8, 0, "Breakfast", ""),
        (8, 0, 9, 0, "Self Study", ""),
        (9, 0, 11, 0, "Workshop", "Room D"),
        (11, 0, 12, 0, "Group Activity", ""),
        (12, 0, 13, 0, "Lunch Break", ""),
        (13, 0, 14, 0, "Class / Lecture", "Room E"),
        (14, 0, 15, 0, "Seminar", "Room E"),
        (15, 0, 16, 0, "Relaxation / Free Time", ""),
        (16, 0, 17, 0, "Sports / Outdoor Activity", ""),
        (17, 0, 17, 30, "Snacks Break", ""),
        (17, 30, 19, 0, "Library Work", ""),
        (19, 0, 20, 0, "Project Work", ""),
        (20, 0, 20, 30, "Relaxation", ""),
        (20, 30, 21, 15, "Dinner", ""),
        (21, 15, 22, 0, "Leisure Activity", ""),
        (22, 0, 22, 30, "Wind down", ""),
    ],
    3: [  # THURSDAY
        (7, 0, 7, 30, "Wake up & freshen up", ""),
        (7, 30, 8, 0, "Breakfast", ""),
        (8, 0, 9, 0, "Class / Lecture", "Room F"),
        (9, 0, 12, 0, "Lab Session", "Lab 2"),
        (12, 0, 13, 0, "Lunch Break", ""),
        (13, 0, 14, 0, "Library Work", ""),
        (14, 0, 15, 0, "Class / Lecture", "Room G"),
        (15, 0, 16, 0, "Workshop", "Room G"),
        (16, 0, 17, 0, "Sports / Outdoor Activity", ""),
        (17, 0, 17, 30, "Snacks Break", ""),
        (17, 30, 19, 0, "Self Study", ""),
        (19, 0, 20, 0, "Creative Work", ""),
        (20, 0, 20, 30, "Relaxation", ""),
        (20, 30, 21, 15, "Dinner", ""),
        (21, 15, 22, 0, "Leisure Activity", ""),
        (22, 0, 22, 30, "Wind down", ""),
    ],
    4: [  # FRIDAY
        (7, 0, 7, 30, "Wake up & freshen up", ""),
        (7, 30, 8, 0, "Breakfast", ""),
        (8, 0, 9, 0, "Self Study", ""),
        (9, 0, 10, 0, "Class / Lecture", "Room H"),
        (10, 0, 11, 0, "Workshop", "Room H"),
        (11, 0, 12, 0, "Creative Work", ""),
        (12, 0, 13, 0, "Lunch Break", ""),
        (13, 0, 16, 0, "Lab Session", "Lab 3"),
        (16, 0, 17, 0, "Sports / Outdoor Activity", ""),
        (17, 0, 17, 30, "Snacks Break", ""),
        (17, 30, 19, 0, "Library Work", ""),
        (19, 0, 20, 0, "Project Work", ""),
        (20, 0, 20, 30, "Relaxation", ""),
        (20, 30, 21, 15, "Dinner", ""),
        (21, 15, 22, 0, "Leisure Activity", ""),
        (22, 0, 22, 30, "Wind down", ""),
    ],
    5: [  # SATURDAY
        (7, 0, 7, 30, "Wake up & freshen up", ""),
        (7, 30, 8, 0, "Breakfast", ""),
        (8, 0, 9, 0, "Self Study", ""),
        (9, 0, 12, 0, "Lab Session", "Lab 4"),
        (12, 0, 13, 0, "Lunch Break", ""),
        (13, 0, 14, 0, "Class / Lecture", "Room I"),
        (14, 0, 15, 0, "Workshop", "Room I"),
        (15, 0, 16, 0, "Seminar", "Room I"),
        (16, 0, 17, 0, "Sports / Outdoor Activity", ""),
        (17, 0, 17, 30, "Snacks Break", ""),
        (17, 30, 19, 0, "Self Study", ""),
        (19, 0, 20, 0, "Creative Work", ""),
        (20, 0, 20, 30, "Relaxation", ""),
        (20, 30, 21, 15, "Dinner", ""),
        (21, 15, 22, 0, "Leisure Activity", ""),
        (22, 0, 22, 30, "Entertainment (movie/series)", ""),
    ],
        6: [  # SUNDAY
        (7, 30, 8, 0, "Wake up & freshen up", ""),
        (8, 0, 9, 0, "Breakfast + Weekly Planning", ""),
        (9, 0, 10, 30, "Reading / Study", ""),
        (10, 30, 12, 0, "Creative Work (art/music)", ""),
        (12, 0, 13, 0, "Lunch Break", ""),
        (13, 0, 14, 30, "Group Activity / Discussion", ""),
        (14, 30, 15, 30, "Relaxation / Free Time", ""),
        (15, 30, 16, 30, "Sports / Outdoor Activity", ""),
        (16, 30, 17, 0, "Snacks Break", ""),
        (17, 0, 18, 30, "Project Work / Planning", ""),
        (18, 30, 19, 30, "Library Work / Reading", ""),
        (19, 30, 20, 30, "Leisure Activity", ""),
        (20, 30, 21, 15, "Dinner", ""),
        (21, 15, 22, 0, "Entertainment (movie/series)", ""),
        (22, 0, 22, 30, "Wind down / Reflection", ""),
    ],
}


# 3. ICS GENERATION (no external libraries required)


def escape_ics_text(text):
    """Escape special characters per RFC 5545."""
    return (
        text.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def format_dt(dt):
    """Format a datetime as an ICS local date-time string."""
    return dt.strftime("%Y%m%dT%H%M%S")


def generate_ics(start_date, end_date, weekly_schedule, output_file):
    lines = []
    lines.append("BEGIN:VCALENDAR")
    lines.append("VERSION:2.0")
    lines.append("PRODID:-//Personal Weekly Timetable//EN")
    lines.append("CALSCALE:GREGORIAN")

    dtstamp = format_dt(datetime.now())

    current_date = start_date
    event_count = 0

    while current_date <= end_date:
        weekday = current_date.weekday()  # Monday=0 ... Sunday=6
        day_events = weekly_schedule.get(weekday, [])

        for (sh, sm, eh, em, title, location) in day_events:
            dt_start = datetime.combine(current_date, datetime.min.time()) \
                       + timedelta(hours=sh, minutes=sm)
            dt_end = datetime.combine(current_date, datetime.min.time()) \
                     + timedelta(hours=eh, minutes=em)

            event_count += 1
            uid = f"{format_dt(dt_start)}-{event_count}@personal-timetable"

            lines.append("BEGIN:VEVENT")
            lines.append(f"UID:{uid}")
            lines.append(f"DTSTAMP:{dtstamp}")
            lines.append(f"DTSTART:{format_dt(dt_start)}")
            lines.append(f"DTEND:{format_dt(dt_end)}")
            lines.append(f"SUMMARY:{escape_ics_text(title)}")
            if location:
                lines.append(f"LOCATION:{escape_ics_text(location)}")
            lines.append("END:VEVENT")

        current_date += timedelta(days=1)

    lines.append("END:VCALENDAR")

    # ICS spec requires CRLF line endings
    ics_content = "\r\n".join(lines) + "\r\n"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(ics_content)

    print(f"Generated {event_count} events.")
    print(f"Saved to: {output_file}")



# 4. RUN


if __name__ == "__main__":
    output_filename = "timetable_20-09-2026_to_17-10-2026_demo.ics"
    generate_ics(START_DATE, END_DATE, WEEKLY_SCHEDULE, output_filename)