"""
Twilio SMS Webhook Server
This Flask app handles incoming SMS messages and adds senders to the mantra distribution list.

To run: python3 webhook_server.py
"""

import json
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

SUBSCRIBERS_FILE = os.path.join(os.path.dirname(__file__), 'subscribers.json')


def load_subscribers():
    """Load the list of subscribers from the JSON file."""
    if not os.path.exists(SUBSCRIBERS_FILE):
        return []
    with open(SUBSCRIBERS_FILE, 'r') as f:
        return json.load(f)


def save_subscribers(subscribers):
    """Save the list of subscribers to the JSON file."""
    with open(SUBSCRIBERS_FILE, 'w') as f:
        json.dump(subscribers, f, indent=2)


@app.route('/sms', methods=['POST'])
def handle_sms():
    """Handle incoming SMS messages."""
    from_number = request.form.get('From')
    body = request.form.get('Body', '').strip().lower()

    # Load current subscribers
    subscribers = load_subscribers()

    # Create response
    resp = MessagingResponse()

    # Handle STOP command
    if body in ['stop', 'unsubscribe', 'cancel']:
        if from_number in subscribers:
            subscribers.remove(from_number)
            save_subscribers(subscribers)
            resp.message("You've been unsubscribed from daily mantras. Text anything to subscribe again.")
        else:
            resp.message("You're not currently subscribed.")
    # Handle subscription
    else:
        if from_number not in subscribers:
            subscribers.append(from_number)
            save_subscribers(subscribers)
            resp.message("Welcome! You've been added to the daily mantra list. You'll receive inspiring messages at 5 AM Pacific Time. Reply STOP to unsubscribe.")
        else:
            resp.message("You're already subscribed! You'll receive daily mantras at 5 AM Pacific Time. Reply STOP to unsubscribe.")

    return str(resp)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return {'status': 'ok', 'subscribers': len(load_subscribers())}


if __name__ == '__main__':
    # Run on port 5000 by default
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
