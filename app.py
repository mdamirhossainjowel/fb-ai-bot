from flask import Flask, request
import requests
import os

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAS6XvwLccsBR2pxIo0YQy37PTWxgclhUZADSHU8oTgRbaWfNZBnGlrugCgPtWWPR6PObC45lD1sUIZAunKtB49zEkSmzpjqAJiF9uLFywkwABTwx3HqJ0gBVUhUkoQuVRbFMZC0QZA9oz52fMRAOMsU4Pj8pFcFsgFVkVWHZCzYZBeIymHWmv97HBXtWgK6s8nTRm71wZDZD"
VERIFY_TOKEN = "my_verify_token"


@app.route("/", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge
    return "Verification failed"


@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print(data)
    return "ok"

    for entry in data.get("entry", []):
        for msg in entry.get("messaging", []):
            if "message" in msg:
                sender = msg["sender"]["id"]
                text = msg["message"].get("text")

                reply = f"You said: {text}"
                send_message(sender, reply)

    return "ok"


def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }

    requests.post(url, json=payload)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)