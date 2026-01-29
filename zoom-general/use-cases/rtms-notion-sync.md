# Sync to Notion

Create Notion pages with meeting summaries using Notion API.

## Overview

This use case demonstrates how to automatically create Notion pages populated with meeting summaries from Zoom Real-Time Meeting Summary (RTMS). After a meeting concludes, the summary is sent to Notion, creating a structured record for knowledge management and team collaboration.

## Prerequisites

- Notion workspace with API access
- Notion API key
- Zoom account with RTMS enabled
- Meeting summary data from Zoom

## JavaScript Implementation

### Installation

```bash
npm install @notionhq/client
```

### Example: Create Notion Page with Meeting Summary

```javascript
const { Client } = require("@notionhq/client");

const notion = new Client({ auth: process.env.NOTION_API_KEY });

async function createMeetingSummaryPage(databaseId, meetingSummary) {
  try {
    const response = await notion.pages.create({
      parent: {
        database_id: databaseId,
      },
      properties: {
        Title: {
          title: [
            {
              text: {
                content: meetingSummary.title,
              },
            },
          ],
        },
        Date: {
          date: {
            start: meetingSummary.date,
          },
        },
        Duration: {
          number: meetingSummary.duration,
        },
        Participants: {
          multi_select: meetingSummary.participants.map((p) => ({
            name: p,
          })),
        },
      },
      children: [
        {
          object: "block",
          type: "heading_2",
          heading_2: {
            rich_text: [
              {
                type: "text",
                text: {
                  content: "Summary",
                },
              },
            ],
          },
        },
        {
          object: "block",
          type: "paragraph",
          paragraph: {
            rich_text: [
              {
                type: "text",
                text: {
                  content: meetingSummary.summary,
                },
              },
            ],
          },
        },
        {
          object: "block",
          type: "heading_2",
          heading_2: {
            rich_text: [
              {
                type: "text",
                text: {
                  content: "Action Items",
                },
              },
            ],
          },
        },
        {
          object: "block",
          type: "bulleted_list_item",
          bulleted_list_item: {
            rich_text: meetingSummary.actionItems.map((item) => ({
              type: "text",
              text: {
                content: item,
              },
            })),
          },
        },
      ],
    });

    console.log("Page created:", response.id);
    return response;
  } catch (error) {
    console.error("Error creating Notion page:", error);
    throw error;
  }
}

// Usage
const meetingSummary = {
  title: "Q1 Planning Meeting",
  date: "2024-01-15",
  duration: 60,
  participants: ["Alice", "Bob", "Charlie"],
  summary:
    "Discussed Q1 goals and resource allocation. Agreed on three main initiatives.",
  actionItems: [
    "Alice to prepare detailed timeline by Jan 20",
    "Bob to review budget allocation",
    "Charlie to schedule follow-up meeting",
  ],
};

createMeetingSummaryPage(process.env.NOTION_DATABASE_ID, meetingSummary);
```

## Python Implementation

### Installation

```bash
pip install notion-client
```

### Example: Create Notion Page with Meeting Summary

```python
from notion_client import Client
from datetime import datetime

notion = Client(auth=os.environ["NOTION_API_KEY"])

def create_meeting_summary_page(database_id, meeting_summary):
    """Create a Notion page with meeting summary details."""
    try:
        response = notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": meeting_summary["title"],
                            }
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": meeting_summary["date"],
                    }
                },
                "Duration": {
                    "number": meeting_summary["duration"],
                },
                "Participants": {
                    "multi_select": [
                        {"name": participant}
                        for participant in meeting_summary["participants"]
                    ]
                },
            },
            children=[
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "Summary",
                                },
                            }
                        ]
                    },
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": meeting_summary["summary"],
                                },
                            }
                        ]
                    },
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "Action Items",
                                },
                            }
                        ]
                    },
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": item,
                                },
                            }
                            for item in meeting_summary["action_items"]
                        ]
                    },
                },
            ],
        )

        print(f"Page created: {response['id']}")
        return response
    except Exception as error:
        print(f"Error creating Notion page: {error}")
        raise


# Usage
meeting_summary = {
    "title": "Q1 Planning Meeting",
    "date": "2024-01-15",
    "duration": 60,
    "participants": ["Alice", "Bob", "Charlie"],
    "summary": "Discussed Q1 goals and resource allocation. Agreed on three main initiatives.",
    "action_items": [
        "Alice to prepare detailed timeline by Jan 20",
        "Bob to review budget allocation",
        "Charlie to schedule follow-up meeting",
    ],
}

create_meeting_summary_page(os.environ["NOTION_DATABASE_ID"], meeting_summary)
```

## Integration with Zoom RTMS

To integrate with Zoom's Real-Time Meeting Summary:

1. **Receive RTMS webhook** - Configure Zoom webhooks to send meeting summaries
2. **Parse summary data** - Extract title, participants, summary text, and action items
3. **Create Notion page** - Use the examples above to create a structured page
4. **Handle errors** - Implement retry logic for failed API calls

## Best Practices

- **Rate limiting**: Respect Notion API rate limits (3-4 requests per second)
- **Error handling**: Implement exponential backoff for retries
- **Data validation**: Validate meeting summary data before sending to Notion
- **Database schema**: Ensure your Notion database has matching properties
- **Async processing**: Use async/await for non-blocking operations

## Resources

- [Notion API Documentation](https://developers.notion.com/)
- [Notion JavaScript Client](https://github.com/makenotion/notion-sdk-js)
- [Notion Python Client](https://github.com/ramnes/notion-sdk-py)
- [Zoom Webhooks](https://developers.zoom.us/docs/api/webhooks/)
