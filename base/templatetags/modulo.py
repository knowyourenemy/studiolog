import datetime
from django import template
from datetime import timedelta

register = template.Library()


@register.filter
def time(num):
    if num is None:
        return "0m"
    hrs = num.days *24 + num.seconds // 3600
    mins = (num.seconds % 3600)//60
    if hrs == 0:
        return str(mins) + "m"
    return str(hrs) + "h" + str(mins) + "m"

@register.filter
def total_time(num):
    if num is None:
        return "0m"
    hours = num.days *24 + num.seconds // 3600
    if hours == 0:
        return str((num.seconds % 3600)//60) + "m"
    return str(hours) + "h"


