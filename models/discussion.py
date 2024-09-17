from config import DOMAIN


class Discussion:
    def __init__(self, id, name, description):
        self.name = name
        self.description = description
        self.link = f"{DOMAIN}/discussion/{str(id)}"
