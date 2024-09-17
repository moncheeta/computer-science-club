from config import (
    GROUP_ID,
    SCHOOLOGY_DOMAIN,
    SCHOOLOGY_API_KEY,
    SCHOOLOGY_API_SECRET,
)
from datetime import datetime
from models import Group, Event, Update, Discussion, Member
from schoolopy import Schoology, Auth
from database import database
import schedule
import time
from threading import Thread


auth = Auth(
    SCHOOLOGY_API_KEY,
    SCHOOLOGY_API_SECRET,
    domain=SCHOOLOGY_DOMAIN,
)
api = Schoology(auth)
api.limit = 64

group = Group(
    api.get_group(GROUP_ID).title, api.get_group(GROUP_ID).description
)
group.projects = database.read()


def get_members():
    for enrolled in api.get_group_enrollments(GROUP_ID):
        member = Member(enrolled.name_display)
        if enrolled.admin == 1:
            group.leaders.append(member)
        else:
            group.members.append(member)


def get_updates():
    for update in api.get_group_updates(GROUP_ID):
        user = api.get_user(update.uid)
        member = Member(user.name_display)
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


update()
schedule.every().hour.do(update)


def run():
    while True:
        schedule.run_pending()
        time.sleep(1 * 60)


scheduler = Thread(target=run, daemon=True)
scheduler.start()
