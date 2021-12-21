from mycroft import MycroftSkill, intent_file_handler, intent_handler
import caldav
from caldav.elements import dav
from secrets import my_username, passwort

class Kalender(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler('kalender.intent')
    def handle_kalender(self, message):
        # Caldav url
        # import secret login code from local file here
        username = my_username
        password = passwort

        url = "https://" + username + ":" + password + "@next.social-robot.info/remote.php/dav"

        # open connection to calendar
        client = caldav.DAVClient(url)
        principal = client.principal()

        # get all available calendars (for this user)
        calendars = principal.calendars()

        # check the calendar events and parse results..
        print(calendars)

        self.speak_dialog('kalender')


def create_skill():
    return Kalender()

