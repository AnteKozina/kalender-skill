import datetime
from datetime import datetime as dt, tzinfo
import caldav
from caldav.elements import dav
from secrets import USERNAME, PASSWORT, CALENDAR_URL
import icalendar
import pytz

Utc = pytz.UTC

class CalendarFunctions:
    '''Contains all functions, that are needed for our calender skill'''

    calendar = None

    def __init__(self, url, calendar_username, calendar_password):
        self.client = caldav.DAVClient(
            url=url,
            username=calendar_username,
            password=calendar_password
        )
        principal = self.client.principal()
        self.calendar = principal.calendars()[0]


    def get_all_events(self):
        '''
        Gets all events from the calendar
            Parameters: None
            Returns: All events in a list
        '''
        events = self.calendar.events()
        events_to_return = []
        for event in events:
            cal = icalendar.Calendar.from_ical(event.data, True)
            for vevent in cal[0].walk("vevent"):
                events_to_return.append(get_calender_events(vevent))

        return events_to_return


    def get_next_event(self):
        '''
        Function to get the next event from the calendar 
        (the event with the next start date in the future)
            Parameters: None
            Returns: Next event
        '''
        all_events = self.get_all_events()
        earliest_event = {}
        time_now = dt.now(tz=None)

        # loop through all events, if start time earlier -> replace earlist_event with current event
        for event in all_events:
            date_of_current_event = event["start"]
            if date_of_current_event > time_now:
                # If earliest event is empty, it will be false
                if bool(earliest_event) is False:
                    earliest_event = event
                else:
                    date_of_earliest_event = earliest_event["start"]
                    if date_of_current_event < date_of_earliest_event:
                        earliest_event = event

        return earliest_event


    def get_all_events_of_day(self, day):
        '''
        Returns all events for a given day
            Parameters: Day in datetime format
            Returns: List of events
        '''
        all_events = self.get_all_events()
        events_on_day = []

        for event in all_events:
            event_date = event["start"]
            if (event_date.year == day.year) and (event_date.month == day.month) and (event_date.day == day.day):
                events_on_day.append(event)

        return events_on_day


def get_calender_events(cal_event):
    '''
    Build a calendar JSON Object from an event object
        Parameters: Calendar Event
        Returns: Dictionary of Events
    '''
    return {
        "summary" : str(cal_event["SUMMARY"]),
        "start" : fix_time_object(cal_event["DTSTART"].dt),
        "end" : fix_time_object(cal_event["DTEND"].dt),
        #"url" : cal_event["url"]
    }


def fix_time_object(time):
    '''
    Removes the timezone information, if timeobject contains timezone
        Parameters: One Datetime Object
        Returns: One Datetime Object without timezone
    '''
    if isinstance(time, datetime.date) and not isinstance(time, datetime.datetime):
        time = dt(time.year, time.month, time.day)
    return time.replace(tzinfo=None)
