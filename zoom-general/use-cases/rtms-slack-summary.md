# Post Summary to Slack

Post meeting summaries to Slack channels using Slack Web API.

## Overview

This use case demonstrates how to integrate Zoom Real-Time Meeting Summary (RTMS) with Slack to automatically post meeting summaries to designated Slack channels. After a meeting concludes, the summary is retrieved from Zoom and posted to Slack using the Slack Web API.

## Prerequisites

- Zoom account with RTMS enabled
- Slack workspace with appropriate permissions
- Slack app with `chat:write` scope
- Zoom API credentials (OAuth token or JWT)
- Slack bot token

## JavaScript Example

Using the `@slack/web-api` package:

```javascript
const { WebClient } = require('@slack/web-api');
const axios = require('axios');

// Initialize Slack client
const slack = new WebClient(process.env.SLACK_BOT_TOKEN);

// Fetch meeting summary from Zoom
async function getMeetingSummary(meetingId, zoomAccessToken) {
  try {
    const response = await axios.get(
      `https://api.zoom.us/v2/meetings/${meetingId}/summary`,
      {
        headers: {
          Authorization: `Bearer ${zoomAccessToken}`,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching meeting summary:', error);
    throw error;
  }
}

// Post summary to Slack
async function postSummaryToSlack(channelId, summary) {
  try {
    const message = {
      channel: channelId,
      blocks: [
        {
          type: 'header',
          text: {
            type: 'plain_text',
            text: '📋 Meeting Summary',
            emoji: true,
          },
        },
        {
          type: 'section',
          fields: [
            {
              type: 'mrkdwn',
              text: `*Meeting ID:*\n${summary.meeting_id}`,
            },
            {
              type: 'mrkdwn',
              text: `*Duration:*\n${summary.duration} minutes`,
            },
          ],
        },
        {
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `*Summary:*\n${summary.summary_text}`,
          },
        },
        {
          type: 'section',
          fields: [
            {
              type: 'mrkdwn',
              text: `*Participants:*\n${summary.participant_count}`,
            },
            {
              type: 'mrkdwn',
              text: `*Date:*\n${new Date(summary.start_time).toLocaleDateString()}`,
            },
          ],
        },
      ],
    };

    const result = await slack.chat.postMessage(message);
    console.log('Message posted successfully:', result.ts);
    return result;
  } catch (error) {
    console.error('Error posting to Slack:', error);
    throw error;
  }
}

// Main function
async function main() {
  const meetingId = process.env.ZOOM_MEETING_ID;
  const zoomAccessToken = process.env.ZOOM_ACCESS_TOKEN;
  const slackChannelId = process.env.SLACK_CHANNEL_ID;

  try {
    const summary = await getMeetingSummary(meetingId, zoomAccessToken);
    await postSummaryToSlack(slackChannelId, summary);
    console.log('Summary posted to Slack successfully');
  } catch (error) {
    console.error('Failed to post summary:', error);
    process.exit(1);
  }
}

main();
```

## Python Example

Using the `slack-sdk` package:

```python
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
from datetime import datetime

# Initialize Slack client
slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

def get_meeting_summary(meeting_id, zoom_access_token):
    """Fetch meeting summary from Zoom API"""
    try:
        headers = {
            "Authorization": f"Bearer {zoom_access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"https://api.zoom.us/v2/meetings/{meeting_id}/summary",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching meeting summary: {e}")
        raise

def post_summary_to_slack(channel_id, summary):
    """Post meeting summary to Slack channel"""
    try:
        # Format the summary message
        message_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📋 Meeting Summary",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Meeting ID:*\n{summary.get('meeting_id', 'N/A')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Duration:*\n{summary.get('duration', 'N/A')} minutes"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Summary:*\n{summary.get('summary_text', 'No summary available')}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Participants:*\n{summary.get('participant_count', 'N/A')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Date:*\n{datetime.fromisoformat(summary.get('start_time', '')).strftime('%Y-%m-%d')}"
                    }
                ]
            }
        ]

        # Post message to Slack
        response = slack_client.chat_postMessage(
            channel=channel_id,
            blocks=message_blocks
        )
        print(f"Message posted successfully: {response['ts']}")
        return response
    except SlackApiError as e:
        print(f"Error posting to Slack: {e}")
        raise

def main():
    """Main function to fetch and post meeting summary"""
    meeting_id = os.environ.get("ZOOM_MEETING_ID")
    zoom_access_token = os.environ.get("ZOOM_ACCESS_TOKEN")
    slack_channel_id = os.environ.get("SLACK_CHANNEL_ID")

    try:
        # Fetch summary from Zoom
        summary = get_meeting_summary(meeting_id, zoom_access_token)
        
        # Post to Slack
        post_summary_to_slack(slack_channel_id, summary)
        print("Summary posted to Slack successfully")
    except Exception as e:
        print(f"Failed to post summary: {e}")
        exit(1)

if __name__ == "__main__":
    main()
```

## Environment Variables

Both examples require the following environment variables:

```bash
ZOOM_MEETING_ID=your_meeting_id
ZOOM_ACCESS_TOKEN=your_zoom_oauth_token
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL_ID=C1234567890
```

## Setup Instructions

### 1. Create Slack App

1. Go to [Slack API Dashboard](https://api.slack.com/apps)
2. Click "Create New App"
3. Select "From scratch"
4. Name your app and select your workspace
5. Go to "OAuth & Permissions"
6. Add `chat:write` scope
7. Install app to workspace
8. Copy the Bot User OAuth Token

### 2. Configure Zoom OAuth

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us)
2. Create a new OAuth app
3. Set redirect URI and get Client ID/Secret
4. Use OAuth flow to obtain access token

### 3. Install Dependencies

**JavaScript:**
```bash
npm install @slack/web-api axios
```

**Python:**
```bash
pip install slack-sdk requests
```

## API Response Format

The Zoom meeting summary API returns:

```json
{
  "meeting_id": "123456789",
  "topic": "Team Standup",
  "start_time": "2024-01-15T10:00:00Z",
  "duration": 30,
  "participant_count": 5,
  "summary_text": "Discussion covered Q1 roadmap, sprint planning, and action items...",
  "key_topics": ["Roadmap", "Sprint Planning", "Action Items"],
  "action_items": [
    {
      "item": "Complete design mockups",
      "owner": "John Doe"
    }
  ]
}
```

## Error Handling

Both examples include error handling for:

- Invalid Zoom credentials
- Invalid Slack channel
- Network failures
- API rate limits

## Best Practices

1. **Rate Limiting**: Implement exponential backoff for API calls
2. **Logging**: Log all API interactions for debugging
3. **Validation**: Validate meeting ID and channel ID before posting
4. **Formatting**: Use Slack Block Kit for rich message formatting
5. **Permissions**: Ensure bot has appropriate Slack workspace permissions
6. **Secrets Management**: Store tokens in secure environment variables or secret manager

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid token" | Verify Slack bot token and Zoom access token are valid |
| "Channel not found" | Ensure bot is invited to the Slack channel |
| "Permission denied" | Check bot has `chat:write` scope in Slack |
| "Meeting not found" | Verify meeting ID is correct and meeting has concluded |

## References

- [Slack Web API Documentation](https://api.slack.com/methods/chat.postMessage)
- [Slack SDK for JavaScript](https://slack.dev/node-sdk/)
- [Slack SDK for Python](https://slack.dev/python-slack-sdk/)
- [Zoom API Documentation](https://developers.zoom.us/docs/api/)
