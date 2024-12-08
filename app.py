import os
import requests
import json
from flask import Flask, request

app = Flask(__name__)

# পেজ অ্যাক্সেস টোকেন লোড করা
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

# JSON ফাইলের পাথ (প্রশ্ন এবং উত্তর সংরক্ষণ করা হয়েছে)
RESPONSES_FILE = "responses.json"

@app.route("/", methods=["GET"])
def verify():
    """Webhook Verification"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and challenge:
        if token == "QEN6uir6Tx4e846PvKf0x1QiVeq-NLv-UjuQjR9RS5M":  # সঠিক Verify Token দিন
            return challenge, 200
        return "Verification token mismatch", 403
    return "Hello, World!", 200

@app.route("/", methods=["POST"])
def webhook():
    """Handles messages from Facebook"""
    data = request.get_json()
    print(f"Received webhook: {data}")

    if data.get('object') == 'page':
        for entry in data['entry']:
            for message in entry.get('messaging', []):
                sender_id = message['sender']['id']
                if 'message' in message and 'text' in message['message']:
                    received_text = message['message']['text'].lower()
                    print(f"Message from {sender_id}: {received_text}")

                    # JSON থেকে উত্তর লোড করা
                    response_text = get_response(received_text)
                    send_message(sender_id, response_text)
    return "EVENT_RECEIVED", 200

def get_response(user_message):
    """JSON ফাইল থেকে প্রশ্নের উত্তর লোড করা"""
    try:
        with open(RESPONSES_FILE, "r", encoding="utf-8") as file:
            responses = json.load(file)
            return responses.get(user_message, "দুঃখিত, আমি বুঝতে পারছি না।")  # ডিফল্ট রেসপন্স
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return "দুঃখিত, বুঝতে পারছি না।"

def send_message(recipient_id, message_text):
    """Send a response to the user"""
    url = f"https://graph.facebook.com/v15.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Message sent: {response.json()}")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    # Flask's built-in development server
    app.run(debug=True, host="0.0.0.0", port=5000)
