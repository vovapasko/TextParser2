from datetime import timedelta, datetime


def format_minutes(minutes):
    if int(minutes) < 10:
        return "0" + str(minutes)  # return '05' instead '5'
    return minutes


def format_hours(hour: int):
    if hour < 10:
        return "0" + str(hour)
    return hour



def split_datetime_to_deltas(start_datetime):
    minutedelta = timedelta(minutes=5)
    date_x = start_datetime
    five_min_timestamps = [date_x]
    while date_x < start_datetime + timedelta(hours=1):
        date_x += minutedelta
        five_min_timestamps.append(date_x)
    return five_min_timestamps


# a = datetime(2020, 11, 21, 23, 0, 0)
#
# res = split_datetime_to_deltas(a)
# print(res)