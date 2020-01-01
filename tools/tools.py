# Program to extract number
# of rows using Python


def format_minutes(minutes):
    if int(minutes) < 10:
        return "0" + str(minutes)  # return '05' instead '5'
    return minutes


def generate_time_intervals(hour):
    """
    returns list of hours in format
    hour_00_00, hour_05_00, ... , hour_55_00, hour+1_00_00
    """
    slices_amount = int(60 / 12)  # take time every 5 minutes
    hours = []
    for i in range(0, 60, slices_amount):
        str_minutes = format_minutes(i)
        string = f"{hour}_{str_minutes}_00"
        hours.append(string)
    hours.append(f"{int(hour) + 1}_00_00") # add the next hour
    return hours
