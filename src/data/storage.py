import json
import os
from src.data.defaults import DEFAULT_VOTES


VOTES_FILE = "votes.json"
PENDING_FILE = "pending.json"
USERS_FILE = "users.json"


def load_data():
    if os.path.exists(VOTES_FILE):
        with open(VOTES_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_VOTES.copy()


def save_data(data):
    with open(VOTES_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_pending():
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, "r") as f:
            return json.load(f)
    return []


def save_pending(pending):
    with open(PENDING_FILE, "w") as f:
        json.dump(pending, f, indent=2)


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)
