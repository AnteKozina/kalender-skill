import caldav
from caldav.elements import dav
from secrets import username, passwort
import icalendar

# Caldav url
# import secret login code from local file here
username = "bw040@hdm-stuttgart.de"
password = "beckerasano"

# url = f"https://{username}:{password}@next.social-robot.info/remote.php/dav"
url = "https://nextcloud.humanoidlab.hdm-stuttgart.de/remote.php/dav/calendars/bw040@hdm-stuttgart.de/personal/"

# open connection to calendar
client = caldav.DAVClient(url=url, username=username, password=passwort)
principal = client.principal()

# get all available calendars (for this user)
calendars = principal.calendars()

# check the calendar events and parse results..
events = calendars[0].events()

parsed_events = []
for event in events:
    event = icalendar.Event()
    print(event)

    '''
    cal = icalendar.Calendar.from_ical(event.data, True)
    url = event.url
    print(cal[0].SUMMARY)
    print("___")
    
    '''
