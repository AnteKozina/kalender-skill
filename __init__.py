from mycroft import MycroftSkill, intent_file_handler, intent_handler
#from secrets import USERNAME, PASSWORT, CALENDAR_URL
#from caldav_starter import CalendarFunctions

class Kalender(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler('kalender.intent')
    def handle_kalender(self, message):
        print(message)
        # Caldav url
        # import secret login code from local file here
        # calendar = CalendarFunctions(CALENDAR_URL, USERNAME, PASSWORT)
        
        self.speak_dialog('TEST')


def create_skill():
    return Kalender()

