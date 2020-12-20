import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

groups_calendar = {'20.Б01-мкн': 'dcdq0k481p3ank5cg4nkjauti8@group.calendar.google.com',
                   '20.Б02-мкн': '',
                   '20.Б03-мкн': '',
                   '20.Б04-мкн': '',
                   '20.Б05-мкн': '',
                   '20.Б06-мкн': ''}
# авторизация сервисного аккаунта
CREDENTIALS_FILE = 'creds.json'
calendar_ident = 'dcdq0k481p3ank5cg4nkjauti8@group.calendar.google.com'
spreadsheet_id = '1wk_ekeLOZF0ZFgX25tqLXSnQtFcFcXByXoo9KPX_zUo'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive',
     'https://www.googleapis.com/auth/calendar',
     'https://www.googleapis.com/auth/calendar.events'],
)
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('calendar', 'v3', http=httpAuth)

event = {
    "summary": 'test_event',
    "description": 'просто тест',
    'start': {
        'dateTime': '2020-12-20T02:00:00',
        'timeZone': 'Europe/Moscow',
    },
    'end': {
        'dateTime': '2020-12-20T05:00:00',
        'timeZone': 'Europe/Moscow',
    }
}
#service.events().insert(calendarId=calendar_ident, body=event).execute()
current_date = datetime.today().date()
print(current_date)

with open('schedule_data2.csv', 'r') as schedule:
    groups = schedule.readline().split('|')
    groups[len(groups) - 1] = groups[len(groups) - 1][:len(groups)+2]
    current_line = schedule.readline().split('|')
    schedule_table = []
    while current_line != ['']:
        schedule_table.append(current_line)
        current_line = schedule.readline().split('|')
events = service.events().list(calendarId='dcdq0k481p3ank5cg4nkjauti8@group.calendar.google.com').execute()
for time_line in schedule_table:
    for group_number in range(len(time_line) - 2):
        current_lecture = time_line[group_number + 2]
        check_event_existence = 0
        current_lecture = 'test_event'
        for current_event in events['items']:
            if current_lecture == current_event['summary']:
                check_event_existence = 1
        if (current_lecture != '') & (current_lecture != '\n') & (check_event_existence == 0):
            event['summary'] = current_lecture
            event['start']['dateTime'] = str(current_date) + 'T' + current_line[1][:5]
            event['end']['dateTime'] = str(current_date) + 'T' + current_line[1][8:13]
            current_group = groups[group_number + 2]
            #service.events().insert(calendarId=groups_calendar[current_group], body=event).execute()

