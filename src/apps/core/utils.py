from datetime import datetime

import jdatetime
from django.utils import timezone


def get_timesince_persian(time):
    time_server = timezone.now()

    diff_time = datetime(
        time_server.year,
        time_server.month,
        time_server.day,
        time_server.hour,
        time_server.minute,
    ) - datetime(time.year, time.month, time.day, time.hour, time.minute)

    diff_time_sec = diff_time.total_seconds()

    day = diff_time.days
    hour = int(diff_time_sec // 3600)
    minute = int(diff_time_sec // 60 % 60)

    if day > 0:
        output = f"{day} روز پیش"
    elif hour > 0:
        output = f"{hour} ساعت پیش"
    elif minute > 0:
        output = f"{minute} دقیقه پیش"
    else:
        output = "لحظاتی پیش"

    return output


def now_shamsi_date():
    now = jdatetime.date.today()
    return now


def convert_str_to_shamsi_date(shamsi_date_str, frmt="%Y-%m-%d"):
    shamsi_date = jdatetime.datetime.strptime(shamsi_date_str, frmt).date()
    return shamsi_date
