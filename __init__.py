from mycroft import MycroftSkill, intent_file_handler, intent_handler
from secrets import USERNAME, PASSWORT, CALENDAR_URL
from caldav_starter import CalendarFunctions
from datetime import datetime
from helper import get_events_on_day_string, get_next_event_string


class Kalender(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    def initialize(self):
        self.register_entity_file('year.entity')
        self.register_entity_file('month.entity')
        self.register_entity_file('day.entity')

    @intent_handler('kalender.next.event.intent')
    def handle_kalender(self, message):
        calendar = CalendarFunctions(CALENDAR_URL, USERNAME, PASSWORT)
        event = calendar.get_next_event()
        response = get_next_event_string(event)
        self.speak_dialog(response)
    
    @intent_handler('kalender.events.on.day.intent')
    def handle_events_on_day(self, message):
        month = message.data.get("month")
        day = message.data.get("day")
        year = message.data.get("year")

        calendar = CalendarFunctions(CALENDAR_URL, USERNAME, PASSWORT)

        if check_month(month) and check_day(day) and check_year(year):
            events = calendar.get_all_events_of_day(datetime(year, month, day))
            response = get_events_on_day_string(events)
            self.speak_dialog(response)
        else:
            self.speak_dialog(f"Date doesnt work!")


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

