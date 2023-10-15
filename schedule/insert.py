from db_main import addMatch, getQualMatchTable
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def schedule_inserter(schedule: list, start_time: datetime, cycle_time: int,
                      am_break_time: datetime, am_break_duration: int,
                      pm_break_time: datetime, pm_break_duration: int,
                      lunch_time: datetime, lunch_duration: int):
    # Verify correct scheduling
    # This inserts matches into the schedule
    match_time = start_time
    real_am_break = None
    real_lunch_break = None
    real_pm_break = None
    for i in range(len(schedule)):
        for j in range(2):
            vert = schedule[i][j][0].split(" ")
            jaune = schedule[i][j][1].split(" ")

            formatted_time = match_time.strftime("%Y-%m-%d %H:%M:%S")
            addMatch(vert[0], vert[1], jaune[0], jaune[1], formatted_time)
            match_time += timedelta(minutes=cycle_time)
            if am_break_time <= match_time < lunch_time and match_time < pm_break_time and real_am_break is None:
                real_am_break = match_time
                match_time += timedelta(minutes=am_break_duration)

            elif am_break_time < match_time < pm_break_time and match_time >= lunch_time and real_lunch_break is None:
                real_lunch_break = match_time
                match_time += timedelta(minutes=lunch_duration)

            elif match_time > am_break_time and match_time > lunch_time and match_time >= pm_break_time and real_pm_break is None:
                real_lunch_break = match_time
                match_time += timedelta(minutes=pm_break_duration)

            else:
                continue

    return real_am_break, real_lunch_break, real_pm_break


def qual_schedule_exporter():
    # Get schedule from db and transform tuples to list
    schedule = getQualMatchTable()
    for i in range(len(schedule)):
        schedule[i] = list(schedule[i])
        schedule[i][0] = schedule[i][0].split(" ")[1]
    # Create the columns names
    columns = ["Heure", "Vert", "Sous-équipe vert", "Jaune", "Sous-équipe jaune"]
    schedule.insert(0, columns)

    # Create a document
    export_file = "BetaHoraire.pdf"
    doc = SimpleDocTemplate(export_file, pagesize=letter)
    table = Table(schedule)

    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.yellowgreen),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.floralwhite),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)

    story = []
    story.append(table)
    doc.build(story)

    print(f"PDF created: {export_file}")
