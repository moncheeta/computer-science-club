class Group:
    def __init__(self, name, description):
        self.name = name
        self.description = description

        self.events = []
        self.updates = []
        self.discussions = []

        self.leaders = []
        self.members = []
