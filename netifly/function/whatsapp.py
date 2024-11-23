from http.server import BaseHTTPRequestHandler
from datetime import datetime
from urllib.parse import parse_qs
import json
import os
from twilio.twig.messaging_response import MessagingResponse

# Timetable data structure
timetable = {
    'monday': {
        'BIT_3_SysDev': ['15:00-16:00 Lecture: ITU/CSL_08107 by Magyabuso, M.'],
    },
    'wednesday': {
        'BIT_3_SysAdmin': ['08:00-09:00 Lecture: ITU_08105 by Simba, F.',
                          '09:00-10:00 Tutorial: LAB_4 by Sheta, F.'],
        'BIT_3_SysDev': ['09:00-10:00 Tutorial: LAB_3 by Sheta, F.',
                         '11:00-12:00 Tutorial: LAB_3 by Nagunwa, T.',
                         '14:00-15:00 Tutorial: LAB_2 by Munissi, H.']
    },
    'thursday': {
        'BIT_3_SysAdmin': ['14:00-15:00 Lecture: 113 by Koloseni, D.',
                          '19:00-20:00 Lecture: ITU/CSL_08110 by Msigwa, F.'],
        'BIT_3_SysDev': ['08:00-09:00 Tutorial: LAB_3 by Mushi, R.',
                         '17:00-18:00 Tutorial: 345 by Selela, M.']
    },
    'friday': {
        'BIT_3_SysAdmin': ['08:00-09:00 Lecture: 113 by Igira, F.',
                          '15:00-16:00 Lecture: IFM_MK1 by Nagunwa, T.',
                          '16:00-17:00 Lecture: IFM_MK1 by Mushi, R.'],
        'BIT_3_SysDev': ['11:00-12:00 Tutorial: 119 by Magyabuso, M.']
    }
}

def get_today_schedule(day):
    if day not in timetable:
        return "No classes scheduled for today!"
    
    schedule = "Today's Schedule:\n\n"
    for program in ['BIT_3_SysDev', 'BIT_3_SysAdmin']:
        if program in timetable[day]:
            schedule += f"{program}:\n"
            schedule += "\n".join(timetable[day][program])
            schedule += "\n\n"
    return schedule.strip()

def get_day_schedule(day):
    schedule = f"Schedule for {day.capitalize()}:\n\n"
    for program in ['BIT_3_SysDev', 'BIT_3_SysAdmin']:
        if program in timetable[day]:
            schedule += f"{program}:\n"
            schedule += "\n".join(timetable[day][program])
            schedule += "\n\n"
    return schedule.strip()

def get_help_message():
    return """Available commands:
- 'today': Get today's schedule
- '[day]': Get schedule for specific day (e.g., 'monday', 'wednesday')
- 'help': Show this help message"""

def handler(event, context):
    # Parse the incoming request
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'body': 'Method Not Allowed'
        }

    # Parse the form data
    body = parse_qs(event['body'])
    incoming_msg = body.get('Body', [''])[0].lower()

    # Create Twilio response
    resp = MessagingResponse()
    msg = resp.message()

    # Handle different commands
    if 'today' in incoming_msg:
        day = datetime.now().strftime('%A').lower()
        msg.body(get_today_schedule(day))
    elif any(day in incoming_msg for day in timetable.keys()):
        day = next(d for d in timetable.keys() if d in incoming_msg)
        msg.body(get_day_schedule(day))
    elif 'help' in incoming_msg:
        msg.body(get_help_message())
    else:
        msg.body("I don't understand that command. Type 'help' for available commands.")

    # Return the response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/xml'
        },
        'body': str(resp)
    }