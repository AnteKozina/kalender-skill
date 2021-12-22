import caldav
from caldav.elements import dav
from secrets import username, passwort, calendar_url
import icalendar
import datetime as dt
import pytz


Utc = pytz.UTC

class Calendar_Functions:

    calendar = None


    # Initiate Class and connect to Calendar
    def __init__(self, url, username, password):
        self.client = caldav.DAVClient(
            url=url,
            username=username,
            password=password
        )
        principal = self.client.principal()
        self.calendar = principal.calendars()[0]
    

    # Get Events and parse them via Helper Function
    def get_all_events(self):
        events = self.calendar.events()
        events_to_return = []
        for event in events:
            cal = icalendar.Calendar.from_ical(event.data, True)
            for vevent in cal[0].walk("vevent"):
                events_to_return.append(get_calender_events(vevent))
        
        return events_to_return
    

    # TODO
    def get_next_event(self):
        all_events = self.get_all_events()
        # initialize with first event
        earliest_event_index = 0

        # loop through all events, if start time earlier -> replace earlist_event with current event
        for e in all_events:
            date_1 = e["start"]
            date_2 = all_events[earliest_event_index]["start"]

            isinstance(date_1, dt.date)
            #print(date_1)
            #print(date_2)

        return earliest_event_index


    # TODO
    def get_all_events_of_day(self):
        pass



'''
HELPER FUNCTIONS
'''

def get_calender_events(cal_event):
    return {
        "summary" : cal_event["SUMMARY"],
        "start" : cal_event["DTSTART"].dt,
        "end" : cal_event["DTEND"].dt
    }