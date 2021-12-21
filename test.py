import caldav
from caldav.elements import dav
from secrets import username, passwort, calendar_url
import icalendar
import datetime as dt
from datetime import datetime
import pytz
from caldav_starter import Calendar_Functions

calendar = Calendar_Functions(calendar_url, username, passwort)
print(calendar.get_all_events()[0]["start"].day)