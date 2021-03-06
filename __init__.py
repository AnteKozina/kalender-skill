"""MYCROFT KALENDER SKILL"""
import math
from datetime import datetime
from logging import info
from mycroft import MycroftSkill, intent_file_handler, intent_handler
from datetime import datetime as dt
from word2number import w2n
import pytz
import caldav
import icalendar

Utc = pytz.UTC

class Kalender(MycroftSkill):
    '''Kalender Skill'''
    def __init__(self):
        MycroftSkill.__init__(self)

        settings_file = self.settings
        self.username = settings_file["skillMetadata"]["sections"][0]["fields"][0]["value"]
        self.password = settings_file["skillMetadata"]["sections"][0]["fields"][1]["value"]
        self.url = settings_file["skillMetadata"]["sections"][0]["fields"][2]["value"]

        info(f"USERNAME = {self.username}")
        info(f"PASSWORD = {self.password}")
        info(f"URL = {self.url}")

    def initialize(self):
        '''Initialization'''
        self.register_entity_file('year.entity')
        self.register_entity_file('month.entity')
        self.register_entity_file('day.entity')

    @intent_handler('kalender.next.event.intent')
    def handle_kalender(self):
        '''Intent Handler: Next event'''
        calendar = CalendarFunctions(self.url, self.username, self.password)
        event = calendar.get_next_event()
        response = get_next_event_string(event)
        self.speak_dialog(response)


    @intent_handler('kalender.events.on.day.intent')
    def handle_events_on_day(self, message):
        '''Intent Handler: Events on day'''
        month = message.data.get("month")
        day = int(message.data.get("day"))
        year = int(message.data.get("year"))

        if math.isnan(year):
            year = w2n.word_to_num(message.data.get("year"))

        if math.isnan(day):
            day = w2n.word_to_num(message.data.get("day"))

        # TO GET NUMBER OF MONTH, E.G. MARCH -> 3
        datetime_object = datetime.strptime(month, "%B")
        month_number = datetime_object.month

        calendar = CalendarFunctions(self.url, self.username, self.password)

        # CHECK IF USEABLE DATE
        if check_month(month) and check_day(day) and check_year(year):
            events = calendar.get_all_events_of_day(datetime(year, month_number, day))
            response = get_events_on_day_string(events)
            self.speak_dialog(response)
        else:
            self.speak_dialog("Date doesnt work")

    @intent_handler('kalender.create.event.intent')
    def handle_events_creation(self, message):
        '''Intent Handler: Creating an Event'''
        date = message.data.get("date")
        start_time = message.data.get("start_time")
        end_time = message.data.get("end_time")
        title = message.data.get("title")

        day_creation_start = datetime(*map(int, date.split(' ')), int(start_time[:2]), int(start_time[2:]))
        day_creation_end = datetime(*map(int, date.split(' ')), int(end_time[:2]), int(end_time[2:]))

        calendar = CalendarFunctions(self.url, self.username, self.password)
        calendar.create_event(title, day_creation_start, day_creation_end)
        self.speak_dialog("Created Event")

    @intent_handler('kalender.delete.event.intent')
    def handle_events_delete(self, message):
        '''Intent Handler: Deleting an Event'''
        date = message.data.get("date")
        title = message.data.get("title")

        if date is not None:
            calendar = CalendarFunctions(self.url, self.username, self.password)
            convert_date = datetime(*map(int, date.split(' ')))
            event = calendar.delete_event(convert_date)

            if event is not None:
                self.speak_dialog("Deleted appointment")

            if event is None:
                self.speak_dialog("No event to delete")

        if title is not None:
            calendar = CalendarFunctions(self.url, self.username, self.password)
            events = calendar.get_all_events()
            has_del = False
            if len(events) > 1:
                for e in events:
                    info(e)
                    if e["summary"] == title:
                        event = calendar.delete_event(e["start"])
                        self.speak_dialog("Deleted appointment")
                        has_del = True
                        break
            if has_del is False:
                self.speak_dialog("No title found to be deleted")

    @intent_handler('kalender.events.rename.event.intent')
    def handle_events_rename(self, message):
        '''Intent Handler: Renaming an Event'''
        date = message.data.get("date")
        title = message.data.get("title")
        old_title = message.data.get("old_title")
        info(old_title)
        if date is not None and title is not None:
            calendar = CalendarFunctions(self.url, self.username, self.password)
            convert_date = datetime(*map(int, date.split(' ')))
            event = calendar.rename_event_by_date(title, convert_date)

            if event is not None:
                self.speak_dialog("Successfully renamed appointment")
            if event is None:
                self.speak_dialog("Didnt rename appointment")

        if old_title is not None and title is not None:
            calendar = CalendarFunctions(self.url, self.username, self.password)
            events = calendar.get_all_events()
            has_changed = False
            if len(events) >= 1:
                for e in events:
                    if e["summary"] == old_title:
                        event = calendar.rename_event_by_date(title, e["start"])
                        self.speak_dialog("Successfully renamed appointment")
                        has_changed = True
                        break
            if has_changed is False:
                self.speak_dialog("No event found to be deleted")


### HELPER FUNCTIONS ###

def create_skill():
    '''Returns calendar'''
    return Kalender()

def check_month(month):
    '''
    Checks if parameter is None, returns bool
    '''
    if month is None:
        return False
    return True

def check_day(day):
    '''
    Check if number is a viable day (between 1 and 31)
        Parameters:
            day: Number
        Returns:
            Boolean
    '''
    if day is None:
        return False
    day = int(day)
    if (day < 1) or (day > 31):
        return False
    return True

def check_year(year):
    '''
    Returns True if year is viable (2022 onwards)
        Parameters:
            year: Number
        Returns:
            Boolean
    '''
    if year is None:
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

    def ical_delete_rename(self, events):
        """
        Parses calendar events from ical to python format
            Parameters:
                events: list of events from calender
            Returns: python list containing the parsed events as dictionaries
        """
        event_on_day = []
        for event in events:
            cal = icalendar.Calendar.from_ical(event.data, True)
            url = event.url
            for vevent in cal[0].walk("vevent"):
                event_details = get_calender_events(vevent)
                event_details["event_url"] = url
                event_on_day.append(event_details)
        return event_on_day

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
            Parameters:
                day: Day in datetime format
            Returns: List of events
        '''
        all_events = self.get_all_events()
        events_on_day = []

        for event in all_events:
            e = event["start"]
            if (e.year == day.year) and (e.month == day.month) and (e.day == day.day):
                events_on_day.append(event)

        return (events_on_day, day)

    def create_event(self, event_name, begin_date, end_date):
        '''
        Create a new event in this calendar
            Parameters:
                event_name: String
                begin_date: Date in datetime format
                            example: datetime.datetime(2022, 2, 25, 10)) -> 25.02.2022 10:00
                end_date: Date in datetime format
            Returns: None
        '''

        helper_calendar = icalendar.Calendar()
        event = icalendar.Event()

        event.add("summary", event_name)
        event.add("dtstart", begin_date)
        event.add("dtend", end_date)

        helper_calendar.add_component(event)
        self.calendar.add_event(helper_calendar)

    def delete_event(self, date):
        '''
        Function for deleting a specific event
            Parameters: 
                date: date of the event
            Returns: Event or None
        '''

        # EARLIEST POSSIBLE TIME OF DAY (00:00:00)
        start_date =  datetime.combine(date, datetime.min.time())

        # LATEST POSSIBLE TIME OF DAY (23:59:59)
        end_date = datetime.combine(date, datetime.max.time())

        # LOOK FOR EVENTS ON DAY
        events = self.calendar.date_search(start=start_date, end=end_date, expand=True)
        event = self.ical_delete_rename(events)

        # DELETING EVENTS
        if event is not None:
            if len(event) == 1:
                event_del = self.calendar.event_by_url(event[0]["event_url"])
                event_del.delete()
                return event

            if len(event) < 1:
                return None

            if len(event) > 1:
                for e in event:
                    event_to_del = self.calendar.event_by_url(e["event_url"])
                    event_to_del.delete()
                    continue
        return None

    def rename_event_by_date(self, title, date):
        '''
        Function for renaming a specific event
            Parameters:
                date: date of the event
                title: title of the event
            Returns: Event or None
        '''

        # EARLIEST POSSIBLE TIME OF DAY (00:00:00)
        start_date =  datetime.combine(date, datetime.min.time())

        # LATEST POSSIBLE TIME OF DAY (23:59:59)
        end_date = datetime.combine(date, datetime.max.time())

        # LOOK FOR EVENTS ON DAY
        events = self.calendar.date_search(start=start_date, end=end_date, expand=True)
        event = self.ical_delete_rename(events)

        # RENAMING THE EVENT
        if event is not None:
            caldav_rename = self.calendar.event_by_url(event[0]["event_url"])
            caldav_rename.vobject_instance.vevent.summary.value = title
            caldav_rename.save()
            return event
        return None

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
    }

def fix_time_object(time):
    '''
    Removes the timezone information, if timeobject contains timezone.
    Tries to get hour of time obj -> If error, convert to datetime with time
        Parameters: One Datetime Object
        Returns: One Datetime Object without timezone
    '''
    try:
        hour = time.hour
    except:
        time = dt(time.year, time.month, time.day)

    # REMOVE TIMEZONE INFORMATION
    time = time.replace(tzinfo=None)
    return time

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
    '''
    Returns the events on a given day
        Parameters:
            events: List of events
        Returns:
            String: Response-String for MyCroft
    '''
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
