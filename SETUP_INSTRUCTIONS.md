# Daily Mantra SMS Setup Instructions

This system allows people to text your Twilio number to automatically subscribe to daily mantras sent at 5 AM Pacific Time.

## Files

- `send_mantras.py` - Schedules daily messages for all subscribers
- `webhook_server.py` - Flask server that handles incoming SMS and manages subscriptions
- `subscribers.json` - List of phone numbers subscribed to receive mantras

## Setup Steps

### 1. Install Dependencies

```bash
pip3 install flask twilio pytz
```

### 2. Start the Webhook Server

You need to expose the webhook server to the internet so Twilio can send incoming SMS to it. Here are your options:

#### Option A: Using ngrok (Easiest for testing)

1. Download ngrok from https://ngrok.com/download
2. Start the webhook server:
   ```bash
   cd ~/Downloads
   python3 webhook_server.py
   ```
3. In another terminal, start ngrok:
   ```bash
   ./ngrok http 5000
   ```
4. Copy the HTTPS URL (e.g., `https://xxxx-xx-xx-xx-xx.ngrok-free.app`)

#### Option B: Deploy to a Cloud Service

Deploy `webhook_server.py` to:
- **Heroku**: Free tier available
- **Railway**: Easy deployment
- **Google Cloud Run**: Serverless option
- **DigitalOcean App Platform**: Simple deployment

### 3. Configure Twilio Webhook

1. Go to your Twilio Console: https://console.twilio.com
2. Navigate to **Phone Numbers** > **Manage** > **Active Numbers**
3. Click on your Twilio phone number (`+14159031907`)
4. Scroll to **Messaging Configuration**
5. Under "A MESSAGE COMES IN":
   - Select "Webhook"
   - Enter your webhook URL: `https://your-url.com/sms`
   - Method: HTTP POST
6. Click **Save**

### 4. Test the Subscription

Send any text message to your Twilio number (`+14159031907`) from a phone, and you should receive a confirmation message. The phone number will be automatically added to `subscribers.json`.

### 5. Schedule Daily Mantras

Run the scheduling script to queue up messages for all subscribers:

```bash
cd ~/Downloads
TWILIO_ACCOUNT_SID="your_account_sid" \
TWILIO_AUTH_TOKEN="your_auth_token" \
TWILIO_FROM_NUMBER="+1xxxxxxxxxx" \
python3 send_mantras.py
```

This will schedule 7 days of mantras for all current subscribers.

## How It Works

### Subscription Flow

1. Someone texts your Twilio number
2. Twilio forwards the message to your webhook server (`/sms` endpoint)
3. The webhook adds their number to `subscribers.json`
4. They receive a confirmation message

### Unsubscribe

Users can text "STOP", "UNSUBSCRIBE", or "CANCEL" to be removed from the list.

### Sending Mantras

- Run `send_mantras.py` to schedule messages for all subscribers
- Messages are scheduled at 5 AM Pacific Time
- The script schedules 7 messages (one per day) for each subscriber

## Automation (Optional)

To automatically schedule mantras weekly:

### Using cron (Mac/Linux)

```bash
# Edit crontab
crontab -e

# Add this line to run every Monday at midnight:
0 0 * * 1 cd ~/Downloads && TWILIO_ACCOUNT_SID="your_account_sid" TWILIO_AUTH_TOKEN="your_auth_token" TWILIO_FROM_NUMBER="+1xxxxxxxxxx" python3 send_mantras.py
```

## Monitoring

- Check webhook health: Visit `https://your-url.com/health` in a browser
- View current subscriber count: Returns JSON with subscriber count
- View subscribers: Check `subscribers.json` file

## Security Notes

- Keep your Twilio credentials secure
- The webhook server has no authentication - consider adding it for production
- `subscribers.json` stores phone numbers in plain text - ensure proper file permissions

## Troubleshooting

**Webhook not receiving messages:**
- Check ngrok is still running
- Verify Twilio webhook URL is correct
- Check webhook server logs

**Messages not sending:**
- Verify Twilio credentials are correct
- Check subscribers.json has valid phone numbers
- Ensure Messaging Service SID is correct

**No subscribers:**
- Verify webhook is properly configured
- Test by sending a text to your Twilio number
- Check webhook server logs for errors
