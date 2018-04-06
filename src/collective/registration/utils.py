# -*- coding: utf-8 -*-

from datetime import datetime


def aivability_registration(period):
    if period.end >= datetime.now().date():
        if nb_place_available(period):
            return True
    return False


def nb_place_available(period):
    if period.available_place > 0:
        return True
    return False
