from datetime import datetime
from mycroft import MycroftSkill, intent_file_handler, intent_handler
from datetime import datetime as dt, tzinfo
from word2number import w2n
#from secrets import USERNAME, PASSWORT, CALENDAR_URL
import pytz
import caldav
import icalendar
import math

#USERNAME = "bw040@hdm-stuttgart.de"
#PASSWORT = "beckerasano2"
CALENDAR_URL = "https://nextcloud.humanoidlab.hdm-stuttgart.de/remote.php/dav/calendars/bw040@hdm-stuttgart.de/personal/"
Utc = pytz.UTC

class Kalender(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    def initialize(self):
        self.register_entity_file('year.entity')
        self.register_entity_file('month.entity')
        self.register_entity_file('day.entity')
        #USERNAME = self.settings.get('my_email_address')
        #PASSWORT = self.settings.get('my_password')

    @intent_handler('kalender.next.event.intent')
    def handle_kalender(self, message):
        USERNAME = self.settings.get('my_email_address')
        PASSWORT = self.settings.get('my_password')
        calendar = CalendarFunctions(CALENDAR_URL, USERNAME, PASSWORT)
        event = calendar.get_next_event()
        response = get_next_event_string(event)
        self.speak_dialog(response)
    
    @intent_handler('kalender.events.on.day.intent')
    def handle_events_on_day(self, message):
        USERNAME = self.settings.get('my_email_address')
        PASSWORT = self.settings.get('my_password')
        month = message.data.get("month")
        day = int(message.data.get("day"))
        year = int(message.data.get("year"))

        if nan_check(year):
            year = w2n.word_to_num(message.data.get("year"))

        if nan_check(day):
            day = w2n.word_to_num(message.data.get("day"))

        datetime_object = datetime.strptime(month, "%B")
        month_number = datetime_object.month

        calendar = CalendarFunctions(CALENDAR_URL, USERNAME, PASSWORT)

        if check_month(month) and check_day(day) and check_year(year):
            events = calendar.get_all_events_of_day(datetime(year, month_number, day))
            response = get_events_on_day_string(events)
            self.speak_dialog(response)
        else:
            self.speak_dialog("Date doesnt work")

def nan_check(number):
    return math.isnan(number)

def create_skill():
    return Kalender()

def check_month(month):
    if month == None:
        return False
    return True

def check_day(day):
    if day == None:
        return False
    day = int(day)
    if (day < 1) or (day > 31):
        return False
    return True

def check_year(year):
    if year == None:
        return False
    year = int(year)
    if year < 2022:
        return False
    return True


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

        return (events_on_day, day)


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
    #if isinstance(time, datetime.date) and not isinstance(time, datetime.datetime):
    time = dt(time.year, time.month, time.day)
    return time.replace(tzinfo=None)
def get_next_event_string(event):
    """
    Takes in an event and returns a string containing the necessary information
    """
    event_name = event["summary"]
    start_time = event["start"]

    year = start_time.year
    month = start_time.strftime("%B")
    day = start_time.day

    time = start_time.strftime("%H:%M")
    return f"Your next appointment is on {month} {day}, {year} at {time} o'clock and is entitled {event_name}."

def get_events_on_day_string(events):
    start_time = events[1]
    year = start_time.year
    month = start_time.strftime("%B")
    day = start_time.day
    return_string = f"On {month} {day}, {year} you have the following appointments: "
    
    # If No events on given day
    if len(events[0]) == 0:
        return f"You have no appointments on {month} {day}, {year}."

    # If only one event on day
    if len(events[0]) == 1:
        return_string = f"You have the following appointment on {month} {day}, {year}: "

    for event in events[0]:
        start_time = event["start"]
        time = start_time.strftime("%H:%M")
        event_name = event["summary"]
        event_string = f" {event_name} at {time} o'clock, "
        return_string += event_string

    return return_string[:-2] + "."
