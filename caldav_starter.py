import caldav
from caldav.elements import dav
from secrets import username, passwort

# Caldav url
# import secret login code from local file here
username = username
password = passwort

url = "https://" + username + ":" + password + "@next.social-robot.info/remote.php/dav"

# open connection to calendar
client = caldav.DAVClient(url)
principal = client.principal()

# get all available calendars (for this user)
calendars = principal.calendars()

# check the calendar events and parse results..
print(calendars)