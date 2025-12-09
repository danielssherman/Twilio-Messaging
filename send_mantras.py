"""
This script uses Twilio's API to send an SMS message immediately.
Before running, set the following environment variables:
- TWILIO_ACCOUNT_SID: your Twilio account SID
- TWILIO_AUTH_TOKEN: your Twilio auth token
"""

import os
from twilio.rest import Client

# Retrieve Twilio credentials from environment variables
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
FROM_NUMBER = "+14159031907"
TO_NUMBER = "+18777804236"

if not (ACCOUNT_SID and AUTH_TOKEN):
    raise EnvironmentError(
        "Twilio credentials are missing. Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN."
    )

# Message to send
MESSAGE = "Breathing in, I calm myself … breathing out, I smile. – Thích Nhất Hạnh"

# Initialize Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

print(f"Sending message to {TO_NUMBER}...")

try:
    message = client.messages.create(
        body=MESSAGE,
        from_=FROM_NUMBER,
        to=TO_NUMBER,
    )
    print(f"✓ Message sent! (SID: {message.sid})")
except Exception as e:
    print(f"✗ Failed to send: {e}")
