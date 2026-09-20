"""
Weekly Timetable -> ICS Generator
----------------------------------
Generates a .ics calendar file for the date range 20/09/2026 to 17/10/2026
based on a fixed weekly schedule (Mon-Sun).

Usage:
    python generate_timetable.py

Output:
    timetable_20-09-2026_to_17-10-2026.ics
"""

from datetime import date, datetime, timedelta

# ---------------------------------------------------------------------------
# 1. CONFIG: date range
# ---------------------------------------------------------------------------
START_DATE = date(2026, 9, 20)   # inclusive
END_DATE   = date(2026, 10, 17)  # inclusive

# ---------------------------------------------------------------------------
# 2. WEEKLY SCHEDULE
# Each entry: (start_hour, start_min, end_hour, end_min, "Title", "Location")
# Location is optional - leave "" if not needed.
# Python's date.weekday(): Monday=0 ... Sunday=6
# ---------------------------------------------------------------------------

WEEKLY_SCHEDULE = {
    0: [  # MONDAY
        (8, 0, 8, 30, "Wake up & freshen up", ""),
        (8, 30, 9, 0, "Breakfast + quick GATE revision", ""),
        (9, 0, 10, 0, "GATE Prep (self-study)", ""),
        (10, 0, 11, 0, "DBMS", "CR3"),
        (11, 0, 12, 0, "IWT", "CR3"),
        (12, 0, 13, 0, "OS", "CR3"),
        (13, 0, 14, 0, "Lunch Break", ""),
        (14, 0, 15, 0, "ML Research (light)", ""),
        (15, 0, 16, 0, "SC", "CR3"),
        (16, 0, 17, 0, "TOC", "CR3"),
        (17, 0, 18, 0, "Cricket / Sports", ""),
        (18, 0, 18, 30, "Break / Snacks", ""),
        (18, 30, 20, 0, "GATE Prep (deep study)", ""),
        (20, 0, 21, 15, "Innovation Club work", ""),
        (21, 15, 21, 30, "Mobile / entertainment buffer", ""),
        (21, 30, 22, 15, "Dinner", ""),
        (22, 15, 23, 0, "ML Research (continue)", ""),
        (23, 0, 23, 30, "Wind down", ""),
    ],
    1: [  # TUESDAY
        (8, 0, 8, 30, "Wake up & freshen up", ""),
        (8, 30, 9, 0, "Breakfast + quick revision", ""),
        (9, 0, 10, 0, "IWT", "CR3"),
        (10, 0, 13, 0, "OS LAB", "PL2"),
        (13, 0, 14, 0, "Lunch Break", ""),
        (14, 0, 15, 0, "GATE Prep (self-study)", ""),
        (15, 0, 16, 0, "TOC", "CR2"),
        (16, 0, 17, 0, "SC", "CR2"),
        (17, 0, 18, 0, "Cricket / Sports", ""),
        (18, 0, 18, 30, "Break", ""),
        (18, 30, 20, 0, "GATE Prep (deep study)", ""),
        (20, 0, 21, 15, "Competitive Coding", ""),
        (21, 15, 21, 30, "Mobile / entertainment", ""),
        (21, 30, 22, 15, "Dinner", ""),
        (22, 15, 23, 0, "Competitive Coding / Video editing", ""),
        (23, 0, 23, 30, "Wind down", ""),
    ],
    2: [  # WEDNESDAY
        (8, 0, 8, 30, "Wake up & freshen up", ""),
        (8, 30, 9, 0, "Breakfast", ""),
        (9, 0, 10, 0, "GATE Prep (deep study)", ""),
        (10, 0, 11, 0, "GATE Prep (continue)", ""),
        (11, 0, 12, 0, "ML Research", ""),
        (12, 0, 13, 0, "ML Research (continue)", ""),
        (13, 0, 14, 0, "Lunch Break", ""),
        (14, 0, 15, 0, "SC", "CR14"),
        (15, 0, 16, 0, "IWT", "CR13"),
        (16, 0, 17, 0, "Entertainment / Mobile / Reels", ""),
        (17, 0, 18, 0, "Cricket / Sports", ""),
        (18, 0, 18, 30, "Break", ""),
        (18, 30, 20, 0, "GATE Prep (light revision)", ""),
        (20, 0, 21, 15, "ML Research", ""),
        (21, 15, 21, 30, "Buffer", ""),
        (21, 30, 22, 15, "Dinner", ""),
        (22, 15, 23, 0, "Video editing / Reels", ""),
        (23, 0, 23, 30, "Wind down", ""),
    ],
    3: [  # THURSDAY
        (8, 0, 8, 30, "Wake up & freshen up", ""),
        (8, 30, 9, 0, "Breakfast + revision", ""),
        (9, 0, 10, 0, "IWT", "CR14"),
        (10, 0, 11, 0, "SC", "CR14"),
        (11, 0, 12, 0, "DBMS", "CR14"),
        (12, 0, 13, 0, "TOC", "CR14"),
        (13, 0, 14, 0, "Lunch Break", ""),
        (14, 0, 15, 0, "GATE Prep", ""),
        (15, 0, 16, 0, "OS", "CR14"),
        (16, 0, 17, 0, "Competitive Coding (light)", ""),
        (17, 0, 18, 0, "Cricket / Sports", ""),
        (18, 0, 18, 30, "Break", ""),
        (18, 30, 20, 0, "GATE Prep (deep study)", ""),
        (20, 0, 21, 15, "Innovation Club work", ""),
        (21, 15, 21, 30, "Mobile / entertainment", ""),
        (21, 30, 22, 15, "Dinner", ""),
        (22, 15, 23, 0, "Competitive Coding (continue)", ""),
        (23, 0, 23, 30, "Wind down", ""),
    ],
    4: [  # FRIDAY
        (8, 0, 8, 30, "Wake up & freshen up", ""),
        (8, 30, 9, 0, "Breakfast + revision", ""),
        (9, 0, 10, 0, "GATE Prep", ""),
        (10, 0, 11, 0, "DBMS", "CR2"),
        (11, 0, 12, 0, "OS", "CR2"),
        (12, 0, 13, 0, "ML Research", ""),
        (13, 0, 14, 0, "Lunch Break", ""),
        (14, 0, 17, 0, "DBMS LAB", "PL1"),
        (17, 0, 18, 0, "Cricket / Sports", ""),
        (18, 0, 18, 30, "Break", ""),
        (18, 30, 20, 0, "GATE Prep (deep study)", ""),
        (20, 0, 21, 15, "ML Research (continue)", ""),
        (21, 15, 21, 30, "Mobile / entertainment", ""),
        (21, 30, 22, 15, "Dinner", ""),
        (22, 15, 23, 0, "Video editing / Reels", ""),
        (23, 0, 23, 30, "Wind down", ""),
    ],
    5: [  # SATURDAY
        (8, 0, 8, 30, "Wake up & freshen up", ""),
        (8, 30, 9, 0, "Breakfast + revision", ""),
        (9, 0, 10, 0, "GATE Prep", ""),
        (10, 0, 13, 0, "PP LAB", "PL1"),
        (13, 0, 14, 0, "Lunch Break", ""),
        (14, 0, 15, 0, "OS", "CR3"),
        (15, 0, 16, 0, "DBMS", "CR3"),
        (16, 0, 17, 0, "TOC", "CR2"),
        (17, 0, 18, 0, "Cricket / Sports", ""),
        (18, 0, 18, 30, "Break", ""),
        (18, 30, 20, 0, "GATE Prep (deep study)", ""),
        (20, 0, 21, 15, "Competitive Coding", ""),
        (21, 15, 21, 30, "Mobile / entertainment", ""),
        (21, 30, 22, 15, "Dinner", ""),
        (22, 15, 23, 0, "Entertainment (movie/series night)", ""),
        (23, 0, 23, 30, "Wind down", ""),
    ],
    6: [  # SUNDAY
        (8, 0, 8, 30, "Wake up & freshen up", ""),
        (8, 30, 9, 30, "Breakfast + weekly planning/review", ""),
        (9, 30, 11, 0, "GATE Prep (mock test / PYQs)", ""),
        (11, 0, 12, 30, "ML Research (deep work)", ""),
        (12, 30, 13, 0, "Buffer", ""),
        (13, 0, 14, 0, "Lunch Break", ""),
        (14, 0, 15, 30, "Competitive Coding (contest slot)", ""),
        (15, 30, 16, 30, "Entertainment / Mobile / Reels", ""),
        (16, 30, 17, 30, "Cricket / Sports", ""),
        (17, 30, 18, 0, "Break", ""),
        (18, 0, 19, 30, "Innovation Club meeting/planning", ""),
        (19, 30, 20, 30, "GATE Prep (revision)", ""),
        (20, 30, 21, 30, "Free time / Video editing", ""),
        (21, 30, 22, 15, "Dinner", ""),
        (22, 15, 23, 0, "Wind down / reading", ""),
    ],
}

# ---------------------------------------------------------------------------
# 3. ICS GENERATION (no external libraries required)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# 4. RUN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    output_filename = "timetable_20-09-2026_to_17-10-2026.ics"
    generate_ics(START_DATE, END_DATE, WEEKLY_SCHEDULE, output_filename)