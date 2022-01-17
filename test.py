import datetime as dt
from datetime import datetime
from secrets import USERNAME, PASSWORT, CALENDAR_URL
import caldav
from caldav.elements import dav
import icalendar
import pytz
from caldav_starter import CalendarFunctions

calendar = CalendarFunctions(CALENDAR_URL, USERNAME, PASSWORT)
response = calendar.get_all_events_of_day(dt.datetime(year=2021, month=12, day=25))
print(response)
print(str(response[0]["summary"]))
# print(calendar.get_next_event())