import os
import requests
from flask import Flask, request

app = Flask(__name__)

# ফেসবুক পেজ এক্সেস টোকেন (এটি .env ফাইল থেকে নেয়া হবে)
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

@app.route('/', methods=['GET'])
def verify():
    """Webhook Verification"""
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args.get("hub.verify_token") == "shahriar_token":
            return request.args["hub.challenge"], 200
        return "Verification token mismatch", 403
    return "Hello, World!", 200

@app.route('/', methods=['POST'])
def webhook():
    """Handles messages from Facebook"""
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for message in entry['messaging']:
                sender_id = message['sender']['id']
                if 'text' in message['message']:
                    response = message['message']['text']
                    send_message(sender_id, response)
    return "EVENT_RECEIVED", 200

def send_message(recipient_id, message_text):
    """Send a response to the user"""
    url = f"https://graph.facebook.com/v15.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": f"আপনার মেসেজ: {message_text}"}
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())

if __name__ == "__main__":
    app.run(port=5000)
