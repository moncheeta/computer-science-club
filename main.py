import os, sys, pathlib

PROJECT_DIR = os.path.join(pathlib.Path(__file__).parent)
sys.path.append(os.path.join(PROJECT_DIR, "config.py"))
sys.path.append(os.path.join(PROJECT_DIR, "models"))
sys.path.append(os.path.join(PROJECT_DIR, "projects.py"))
sys.path.append(os.path.join(PROJECT_DIR, "schoology.py"))
from config import DOMAIN
from models import Group, Project
from database import database
from schoology import group
from flask import Flask, request, redirect, abort, render_template, session
from cachecontrol import CacheControl

app = Flask(__name__)
app.secret_key = DOMAIN


@app.route("/")
def index():
    return render_template(
        "home.html", group=group, account=session.get("name")
    )


@app.route("/updates")
def updates():
    return render_template(
        "updates.html", group=group, account=session.get("name")
    )


@app.route("/discussions")
def discussions():
    return render_template(
        "discussions.html", group=group, account=session.get("name")
    )


@app.route("/projects", methods=["GET", "POST"])
def projects():
    return render_template(
        "projects.html", group=group, create=False, account=session.get("name")
    )


@app.route("/projects/add", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        if not session.get("name"):
            return abort(401)
        name = request.form["name"].rstrip()
        description = request.form["description"].rstrip()
        if description == "":
            description = None
        authors = request.form["authors"]
        for author in authors:
            author = author.rstrip()
        source = request.form["source"].rstrip()
        if source == "":
            source = None
        project = Project(name, description, [authors], source)
        database.add(project)
        return redirect("/projects")
    return render_template(
        "projects.html", group=group, create=True, account=session.get("name")
    )


@app.route("/members")
def members():
    return render_template(
        "members.html", group=group, account=session.get("name")
    )


import requests
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token

GOOGLE_CLIENT_ID = (
    "861597772911-7k5ipk33tj84ubts3oulmqt6jp053hnr.apps.googleusercontent.com"
)
GOOGLE_CLIENT_SECRETS_FILE = os.path.join(PROJECT_DIR, "google_auth.json")
GOOGLE_AUTH_SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_secrets_file(
    client_secrets_file=GOOGLE_CLIENT_SECRETS_FILE,
    scopes=GOOGLE_AUTH_SCOPES,
    redirect_uri=DOMAIN + "/login/callback",
)


@app.route("/login")
def login():
    auth_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(auth_url)


@app.route("/login/callback")
def login_callback():
    flow.fetch_token(authorization_response=request.url)
    if not session["state"] == request.args["state"]:
        abort(500)
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session
    )
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
    )
    session["name"] = id_info.get("name")
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
