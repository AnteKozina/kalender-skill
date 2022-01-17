import datetime as dt
from datetime import datetime
from secrets import USERNAME, PASSWORT, CALENDAR_URL
from tracemalloc import start
import caldav
from caldav.elements import dav
import icalendar
import pytz
from caldav_starter import CalendarFunctions
from helper import get_next_event_string, get_events_on_day_string

calendar = CalendarFunctions(CALENDAR_URL, USERNAME, PASSWORT)
response = calendar.get_all_events_of_day(datetime(2022, 3, 1))

print(get_events_on_day_string(response))