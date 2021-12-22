import datetime as dt
from datetime import datetime
from secrets import USERNAME, PASSWORT, CALENDAR_URL
import caldav
from caldav.elements import dav
import icalendar
import pytz
from caldav_starter import CalendarFunctions

calendar = CalendarFunctions(CALENDAR_URL, USERNAME, PASSWORT)
print(calendar.get_next_event())
