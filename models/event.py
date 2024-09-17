from config import DOMAIN


class Event:
    def __init__(self, id, name, description, start, end=None):
        self.name = name
        self.description = description
        self.link = f"{DOMAIN}/event/{str(id)}"
        self.start = start
        self.end = end
        if end and (
            self.end.year != self.start.year
            or self.end.month != self.start.month
            or self.end.day != start.day
        ):
            self.differentDay = True
        else:
            self.differentDay = False
