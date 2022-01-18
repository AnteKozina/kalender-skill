from mycroft import MycroftSkill, intent_file_handler, intent_handler
from caldav import caldav

class Kalender(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler('kalender.intent')
    def handle_kalender(self, message):
        self.speak_dialog('kalender')


def create_skill():
    return Kalender()

