from config import SCHOOLOGY_DOMAIN


class Discussion:
    def __init__(self, id, name, description):
        self.name = name
        self.description = description
        self.link = f"{SCHOOLOGY_DOMAIN}/discussion/{str(id)}"
