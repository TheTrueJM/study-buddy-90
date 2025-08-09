import time
import requests

BASE = "http://127.0.0.1:8000"

def post(path, json=None, params=None):
    r = requests.post(f"{BASE}{path}", json=json, params=params)
    try:
        data = r.json()
    except Exception:
        data = r.text
    print("POST", path, "->", r.status_code, data)
    return r

def get(path, params=None):
    r = requests.get(f"{BASE}{path}", params=params)
    try:
        data = r.json()
    except Exception:
        data = r.text
    print("GET ", path, "->", r.status_code, data)
    return r

def delete(path, params=None):
    r = requests.delete(f"{BASE}{path}", params=params)
    try:
        data = r.json()
    except Exception:
        data = r.text
    print("DEL ", path, "->", r.status_code, data)
    return r

def main():
    ts = str(int(time.time()))
    # 1) Create two users (adjust if you already have them)
    r = post("/students", {
        "name": f"alice_{ts}",
        "password": "secret",
        "fax_n": "", "pager_n": "", "avatar_url": ""
    }); alice_id = r.json()["id"]

    r = post("/students", {
        "name": f"bob_{ts}",
        "password": "secret",
        "fax_n": "", "pager_n": "", "avatar_url": ""
    }); bob_id = r.json()["id"]

    # 2) Send a short pager message from Alice -> Bob
    r = post("/messages", {"sender_id": alice_id, "recipient_id": bob_id, "body": "meet @ 3pm?"})
    msg_id = r.json()["id"]

    # 3) Bob checks inbox; Alice checks outbox
    get(f"/users/{bob_id}/inbox")
    get(f"/users/{alice_id}/outbox")

    # 4) Bob sees unread count
    get(f"/users/{bob_id}/unread-count")

    # 5) Mark the message as read (Bob reads it)
    post(f"/messages/{msg_id}/read")

    # 6) Unread count should drop to 0
    get(f"/users/{bob_id}/unread-count")

    # 7) Conversation view between Alice & Bob
    get(f"/users/{alice_id}/conversation/{bob_id}", params={"limit": 50})

    # 8) Try to send an over-long message (should 400)
    too_long = "X" * 161
    post("/messages", {"sender_id": alice_id, "recipient_id": bob_id, "body": too_long})

    # 9) Delete the original message (as Alice, the sender)
    delete(f"/messages/{msg_id}", params={"acting_user_id": alice_id})

    # 10) Inbox after delete (should no longer include that message)
    get(f"/users/{bob_id}/inbox")

if __name__ == "__main__":
    main()
