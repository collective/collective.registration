# encoding: utf-8
from datetime import datetime


def aivability_registration(period):
    if period.end >= datetime.now().date():
        if nb_place_available(period):
            return True
    return False

def nb_place_available(period):
    """
    method for calculate number place available
    TODO make this; return always true for wip
    :param period:
    :return: True if place available False if not
    """
    return True
