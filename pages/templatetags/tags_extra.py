# -*- coding: utf-8 -*-
import datetime

from django import template
from django.conf import settings
from django.urls.base import reverse

register = template.Library()

# how to use in template:
# {% load template_tags %}
# make available on function like:
# {% navactive request 'home-public' %}

@register.simple_tag
def navactive(request, urls):
    # returns active navigation button
    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""

@register.simple_tag
def navactive_with_arg(request, urls, arg):
    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""

@register.simple_tag
def getCopyrightYears():
    """
    Gets the Copyrigth Years. like "2009 - 2012".
    If no COPY_START_YEAR is given in the settings, it returns thisYear.
    else COPY_START_YEAR - thisYear

    Example :

        {{ request|getCopyrightYears }}
    """
    thisYear = datetime.datetime.now().year
    if hasattr(settings, "COPY_START_YEAR"):
        copyYearStart = getattr(settings, "COPY_START_YEAR", )
        if copyYearStart is not None and copyYearStart != thisYear:
            return "%s - %s" % (str(settings.COPY_START_YEAR), str(thisYear))
    return str(thisYear)