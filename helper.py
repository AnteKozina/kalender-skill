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


