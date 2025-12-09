# Daily Mantras SMS Project

This folder contains everything you need to run your daily mantra SMS service.

## Project Files

- **send_mantras.py** - Schedules daily mantras for all subscribers
- **webhook_server.py** - Handles incoming SMS and manages subscriptions
- **subscribers.json** - List of phone numbers subscribed to receive mantras
- **ngrok** - Tool to expose your webhook to the internet
- **SETUP_INSTRUCTIONS.md** - Detailed setup guide

## Quick Start

### To Schedule Mantras for All Subscribers

```bash
cd ~/Desktop/daily-mantras
TWILIO_ACCOUNT_SID="your_account_sid" \
TWILIO_AUTH_TOKEN="your_auth_token" \
TWILIO_FROM_NUMBER="+1xxxxxxxxxx" \
python3 send_mantras.py
```

### To Start the Webhook Server

```bash
cd ~/Desktop/daily-mantras
python3 webhook_server.py
```

In another terminal:
```bash
cd ~/Desktop/daily-mantras
./ngrok http 5000
```

## Current Status

**Webhook Server:** Running ✓
**ngrok Tunnel:** Running ✓
**Webhook URL:** https://skinflinty-spirochetotic-kolten.ngrok-free.dev/sms
**Twilio Number:** +1 (415) 903-1907

## How It Works

1. Someone texts your Twilio number (+14159031907)
2. Twilio forwards the message to your webhook
3. The webhook adds them to `subscribers.json`
4. When you run `send_mantras.py`, it schedules messages for all subscribers

## Managing Subscribers

- **View subscribers:** Open `subscribers.json`
- **Add manually:** Add phone number to the JSON array (format: "+14155551234")
- **Remove:** Delete the phone number from the JSON array

## Twilio Configuration

Your Twilio number is configured to send incoming SMS to:
`https://skinflinty-spirochetotic-kolten.ngrok-free.dev/sms`

If you restart ngrok, you'll get a new URL and need to update it in Twilio:
https://console.twilio.com/us1/develop/phone-numbers/manage/active

## Notes

- Keep terminal windows open while the webhook is active
- The ngrok URL changes each time you restart (upgrade to paid for static URL)
- For production, deploy webhook_server.py to Heroku/Railway for a permanent URL
