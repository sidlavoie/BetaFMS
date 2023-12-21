from db_main import *
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from schedule.scheduler import *
import schedule.scheduleConfig

teamColors = ["Rouge", "Bleu", "Violet", "Orange"]

schedule_conf = schedule.scheduleConfig.ScheduleConfiguration()


# This function is really important. It calls the scheduler and inserts the matches into the database with a timestamp
def schedule_inserter(start_time: datetime, cycle_time: int,
                      am_break_time: datetime, am_break_duration: int,
                      pm_break_time: datetime, pm_break_duration: int,
                      lunch_time: datetime, lunch_duration: int):
    # Reset previous schedule
    reset_qual_matches()
    # Create a schedule
    schedule = generate_schedule(getTeamsNumberList(), teamColors)
    match_time = start_time
    real_am_break = None
    real_lunch_break = None
    real_pm_break = None
    #Insert into matches
    for i in range(len(schedule)):
        for j in range(len(schedule[i])):
            vert = schedule[i][j][0].split(" ")
            jaune = schedule[i][j][1].split(" ")

            formatted_time = match_time.strftime("%Y-%m-%d %H:%M:%S")
            addMatch(vert[0], vert[1], jaune[0], jaune[1], formatted_time)
            match_time += timedelta(minutes=cycle_time)
            if am_break_time <= match_time < lunch_time and match_time < pm_break_time and real_am_break is None and am_break_duration != 0:
                real_am_break = match_time
                addMatch("Pause", "Pause", "Pause", "Pause", match_time.strftime("%Y-%m-%d %H:%M:%S"))
                match_time += timedelta(minutes=am_break_duration)

            elif am_break_time < match_time < pm_break_time and match_time >= lunch_time and real_lunch_break is None and lunch_duration != 0:
                real_lunch_break = match_time
                addMatch("Dîner", "Dîner", "Dîner", "Dîner", match_time.strftime("%Y-%m-%d %H:%M:%S"))
                match_time += timedelta(minutes=lunch_duration)

            elif match_time > am_break_time and match_time > lunch_time and match_time >= pm_break_time and real_pm_break is None and pm_break_duration != 0:
                real_pm_break = match_time
                addMatch("Pause", "Pause", "Pause", "Pause", match_time.strftime("%Y-%m-%d %H:%M:%S"))
                match_time += timedelta(minutes=pm_break_duration)

            else:
                continue

    return real_am_break, real_lunch_break, real_pm_break


def qual_schedule_exporter():
    # Get schedule from db and transform tuples to list
    schedule = ""
    schedule = getQualMatchTable()
    for i in range(len(schedule)):
        schedule[i] = list(schedule[i])
        schedule[i][0] = schedule[i][0].split(" ")[1]

    # Specify hex color values
    green_hex = '#16E00F'
    yellow_hex = '#E0E200'

    # Create the columns names
    columns = ["Heure", "Vert", "Sous-équipe vert", "Jaune", "Sous-équipe jaune"]
    schedule.insert(0, columns)

    # Title
    title_style = getSampleStyleSheet()["Title"]
    title_text = f'Horaire du {schedule_conf.day.strftime("%Y-%m-%d")}'
    title_paragraph = Paragraph(title_text, title_style)

    # Create a document
    export_file = "BetaHoraire.pdf"
    doc = SimpleDocTemplate(export_file, pagesize=letter)
    table = Table(schedule)

    # Define column ranges for different colors
    white_columns = [0]
    green_columns = [1, 2]
    yellow_columns = [3, 4]

    # Apply different colors to different column ranges
    style = TableStyle([('BACKGROUND', (col, 0), (col, -1), colors.white) for col in white_columns] +
                       [('BACKGROUND', (col, 0), (col, -1), green_hex) for col in green_columns] +
                       [('BACKGROUND', (col, 0), (col, -1), yellow_hex) for col in yellow_columns] +
                       [('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.floralwhite),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]
                       )
    table.setStyle(style)

    # Add title and table to the story
    story = [title_paragraph, table]

    doc.build(story)

    print(f"PDF created: {export_file}")
    return export_file
