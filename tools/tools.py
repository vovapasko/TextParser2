from datetime import timedelta, datetime


def format_minutes(minutes):
    if int(minutes) < 10:
        return "0" + str(minutes)  # return '05' instead '5'
    return minutes


def format_hours(hour: int):
    if hour < 10:
        return "0" + str(hour)
    return hour


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
    hours.append(f"{format_hours(int(hour) + 1)}_00_00")  # add the next hour
    return hours


def split_datetime_to_deltas(start_datetime):
    minutedelta = timedelta(minutes=5)
    date_x = start_datetime
    five_min_timestamps = [str(date_x)]
    while date_x < start_datetime + timedelta(hours=1):
        date_x += minutedelta
        five_min_timestamps.append(str(date_x))
    return five_min_timestamps


a = datetime(2020, 11, 21, 23, 0, 0)

res = split_datetime_to_deltas(a)
print(res)