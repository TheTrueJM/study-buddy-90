import requests
import json

BASE = "http://127.0.0.1:8000"

def main():
    # Create two test users
    u1 = requests.post(f"{BASE}/auth/signup", json={
        "student_id": 99911111,
        "name": "TooLongUser1",
        "password": "pass123"
    })
    print("Signup 1:", u1.status_code, u1.json())

    u2 = requests.post(f"{BASE}/auth/signup", json={
        "student_id": 99922222,
        "name": "TooLongUser2",
        "password": "pass123"
    })
    print("Signup 2:", u2.status_code, u2.json())

    pager2 = u2.json()["student"]["pager_n"]

    # Create a message that's 161 characters long
    too_long_body = "X" * 161

    r = requests.post(f"{BASE}/messages", json={
        "sender_id": 99911111,
        "recipient_pager": pager2,
        "body": too_long_body
    })

    print("Send message:", r.status_code)
    print(json.dumps(r.json(), indent=2))

if __name__ == "__main__":
    main()

