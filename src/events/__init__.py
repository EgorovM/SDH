from enum import Enum


class Event(Enum):
    COMMON = 0
    OFF_TOP = 1
    INFORMATION = 2
    CONSULTATION = 3

    @staticmethod
    def from_number(number):
        for event in Event:
            if event.value == number:
                return event
