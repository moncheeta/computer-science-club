from config import DOMAIN, GROUP_ID, SCHOOLOGY_API_KEY, SCHOOLOGY_API_SECRET
from datetime import datetime
from models import Group, Event, Update, Discussion, Member
from schoolopy import Schoology, Auth
from database import database


auth = Auth(
    SCHOOLOGY_API_KEY,
    SCHOOLOGY_API_SECRET,
    domain=DOMAIN,
)
api = Schoology(auth)
api.limit = 64

group = Group(
    api.get_group(GROUP_ID).title, api.get_group(GROUP_ID).description
)


def get_members():
    for enrolled in api.get_group_enrollments(GROUP_ID):
        member = Member(enrolled.name_display)
        if enrolled.admin == 1:
            group.leaders.append(member)
        else:
            group.members.append(member)


def find_member(name):
    for member in group.members:
        if member.name == name:
            return member
    return None


def get_updates():
    for update in api.get_group_updates(GROUP_ID):
        user = api.get_user(update.uid)
        member = find_member(user.name_display)
        if not member:
            continue
        created = datetime.utcfromtimestamp(int(update.created))
        group.updates.append(Update(member, update.body, created))


def get_events():
    for event in api.get_group_events(GROUP_ID):
        start = datetime.strptime(event.start, "%Y-%m-%d %H:%M:%S")
        end = None
        if event.has_end:
            end = datetime.strptime(event.end, "%Y-%m-%d %H:%M:%S")
        event = Event(event.id, event.title, event.description, start, end)
        group.events.append(event)


def get_discussions():
    for discussion in api.get_group_discussions(GROUP_ID):
        group.discussions.append(
            Discussion(discussion.id, discussion.title, discussion.body)
        )


def update():
    get_members()
    get_updates()
    get_events()
    get_discussions()
    group.projects = database.read()


update()
