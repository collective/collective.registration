# -*- coding: utf-8 -*-

from datetime import datetime


def availability_registration(period):
    if period.end >= datetime.now().date():
        if nb_places_available(period):
            return True
    return False


def nb_places_available(period):
    if period.available_places > 0:
        return True
    return False
