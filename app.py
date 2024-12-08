import os
import requests
from flask import Flask, request
from urllib.parse import quote as url_quote

app = Flask(__name__)

# পেজ অ্যাক্সেস টোকেন লোড করা
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

@app.route("/", methods=["GET"])
def verify():
    """Webhook Verification"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and challenge:
        if token == "my_secure_token":  # আপনার Verify Token
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
                    received_text = message['message']['text']
                    print(f"Message from {sender_id}: {received_text}")
                    send_message(sender_id, f"আপনার মেসেজ: {received_text}")
    return "EVENT_RECEIVED", 200

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


