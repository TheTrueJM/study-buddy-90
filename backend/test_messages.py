import requests

BASE = "http://127.0.0.1:8000"

def post(path, json=None, params=None):
    r = requests.post(f"{BASE}{path}", json=json, params=params)
    try:
        print("POST", path, "->", r.status_code, r.json())
        return r.json()
    except:
        print("POST", path, "->", r.status_code, r.text)
        return None

def get(path, params=None):
    r = requests.get(f"{BASE}{path}", params=params)
    try:
        print("GET ", path, "->", r.status_code, r.json())
        return r.json()
    except:
        print("GET ", path, "->", r.status_code, r.text)
        return None

def delete(path, params=None):
    r = requests.delete(f"{BASE}{path}", params=params)
    try:
        print("DEL ", path, "->", r.status_code, r.json())
        return r.json()
    except:
        print("DEL ", path, "->", r.status_code, r.text)
        return None

def main():
    # 1) Create two users with fixed student IDs
    s1 = post("/auth/signup", {
        "student_id": 11555777,
        "name": "UserOne",
        "password": "pass123"
    })
    s2 = post("/auth/signup", {
        "student_id": 11777555,
        "name": "UserTwo",
        "password": "pass123"
    })

    # Extract pager numbers from signup response
    pager1 = s1["student"]["pager_n"]
    pager2 = s2["student"]["pager_n"]

    # 2) UserOne sends message to UserTwo via pager_n
    msg = post("/messages", {
        "sender_id": 11555777,
        "recipient_pager": pager2,
        "body": "Hey from my pager!"
    })
    msg_id = msg["message_id"]

    # 3) Check inbox/outbox
    get(f"/users/{11777555}/inbox")
    get(f"/users/{11555777}/outbox")

    # 4) Check unread count for UserTwo
    get(f"/users/{11777555}/unread-count")

    # 5) Mark as read
    post(f"/messages/{msg_id}/read")

    # 6) Check unread count again
    get(f"/users/{11777555}/unread-count")

    # 7) Conversation between users
    get(f"/users/{11555777}/conversation/{11777555}", params={"limit": 50})

if __name__ == "__main__":
    main()

