# Generate Meeting Minutes

## Brief
Generate formal meeting minutes from RTMS (Real-Time Messaging Service) transcripts. This use case demonstrates how to process meeting transcripts and create structured, professional meeting minutes with key sections including attendees, agenda items, decisions, and action items.

## Overview
Meeting minutes are essential documentation that capture the essence of a meeting. This use case shows how to:
- Parse RTMS transcript data
- Extract key information (attendees, topics, decisions)
- Structure data into formal meeting minutes format
- Generate professional documentation

## JavaScript Example

```javascript
const axios = require('axios');

/**
 * Generate meeting minutes from RTMS transcript
 * @param {string} meetingId - The Zoom meeting ID
 * @param {string} accessToken - Zoom API access token
 * @returns {Promise<Object>} Structured meeting minutes
 */
async function generateMeetingMinutes(meetingId, accessToken) {
  try {
    // Fetch transcript from Zoom API
    const transcriptResponse = await axios.get(
      `https://api.zoom.us/v2/meetings/${meetingId}/recordings`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    const recordingFiles = transcriptResponse.data.recording_files;
    const transcriptFile = recordingFiles.find(
      (file) => file.file_type === 'TRANSCRIPT'
    );

    if (!transcriptFile) {
      throw new Error('No transcript found for this meeting');
    }

    // Fetch the actual transcript content
    const transcriptContent = await axios.get(transcriptFile.download_url, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    // Parse transcript and extract key information
    const minutes = parseTranscript(transcriptContent.data);

    return minutes;
  } catch (error) {
    console.error('Error generating meeting minutes:', error.message);
    throw error;
  }
}

/**
 * Parse transcript and structure into meeting minutes
 * @param {Object} transcript - Raw transcript data
 * @returns {Object} Structured meeting minutes
 */
function parseTranscript(transcript) {
  const minutes = {
    meetingTitle: transcript.topic || 'Meeting Minutes',
    date: new Date(transcript.start_time).toLocaleDateString(),
    time: new Date(transcript.start_time).toLocaleTimeString(),
    attendees: extractAttendees(transcript),
    agenda: extractAgendaItems(transcript),
    decisions: extractDecisions(transcript),
    actionItems: extractActionItems(transcript),
    nextMeeting: null,
  };

  return minutes;
}

/**
 * Extract attendees from transcript
 * @param {Object} transcript - Raw transcript data
 * @returns {Array} List of attendees
 */
function extractAttendees(transcript) {
  const attendees = [];
  const speakers = new Set();

  if (transcript.participants) {
    transcript.participants.forEach((participant) => {
      speakers.add(participant.name);
    });
  }

  return Array.from(speakers).map((name) => ({
    name,
    role: 'Participant',
  }));
}

/**
 * Extract agenda items from transcript
 * @param {Object} transcript - Raw transcript data
 * @returns {Array} List of agenda items
 */
function extractAgendaItems(transcript) {
  const agendaItems = [];
  const sentences = transcript.text.split(/[.!?]+/);

  // Simple heuristic: sentences with certain keywords are agenda items
  const agendaKeywords = [
    'discuss',
    'review',
    'update',
    'agenda',
    'topic',
    'item',
  ];

  sentences.forEach((sentence) => {
    const lowerSentence = sentence.toLowerCase().trim();
    if (
      agendaKeywords.some((keyword) => lowerSentence.includes(keyword)) &&
      sentence.length > 20
    ) {
      agendaItems.push({
        item: sentence.trim(),
        discussed: true,
      });
    }
  });

  return agendaItems;
}

/**
 * Extract decisions from transcript
 * @param {Object} transcript - Raw transcript data
 * @returns {Array} List of decisions made
 */
function extractDecisions(transcript) {
  const decisions = [];
  const sentences = transcript.text.split(/[.!?]+/);

  // Keywords indicating decisions
  const decisionKeywords = [
    'decided',
    'agreed',
    'approved',
    'will',
    'shall',
    'resolved',
  ];

  sentences.forEach((sentence) => {
    const lowerSentence = sentence.toLowerCase().trim();
    if (
      decisionKeywords.some((keyword) => lowerSentence.includes(keyword)) &&
      sentence.length > 20
    ) {
      decisions.push({
        decision: sentence.trim(),
        date: new Date().toISOString(),
      });
    }
  });

  return decisions;
}

/**
 * Extract action items from transcript
 * @param {Object} transcript - Raw transcript data
 * @returns {Array} List of action items
 */
function extractActionItems(transcript) {
  const actionItems = [];
  const sentences = transcript.text.split(/[.!?]+/);

  // Keywords indicating action items
  const actionKeywords = [
    'action',
    'todo',
    'follow up',
    'send',
    'prepare',
    'create',
    'schedule',
  ];

  sentences.forEach((sentence) => {
    const lowerSentence = sentence.toLowerCase().trim();
    if (
      actionKeywords.some((keyword) => lowerSentence.includes(keyword)) &&
      sentence.length > 20
    ) {
      actionItems.push({
        item: sentence.trim(),
        owner: 'TBD',
        dueDate: null,
        status: 'Open',
      });
    }
  });

  return actionItems;
}

/**
 * Format meeting minutes as markdown
 * @param {Object} minutes - Structured meeting minutes
 * @returns {string} Formatted markdown
 */
function formatMinutesAsMarkdown(minutes) {
  let markdown = `# ${minutes.meetingTitle}\n\n`;
  markdown += `**Date:** ${minutes.date}\n`;
  markdown += `**Time:** ${minutes.time}\n\n`;

  markdown += `## Attendees\n`;
  minutes.attendees.forEach((attendee) => {
    markdown += `- ${attendee.name} (${attendee.role})\n`;
  });

  markdown += `\n## Agenda\n`;
  minutes.agenda.forEach((item, index) => {
    markdown += `${index + 1}. ${item.item}\n`;
  });

  markdown += `\n## Decisions\n`;
  if (minutes.decisions.length > 0) {
    minutes.decisions.forEach((decision) => {
      markdown += `- ${decision.decision}\n`;
    });
  } else {
    markdown += `- No decisions recorded\n`;
  }

  markdown += `\n## Action Items\n`;
  if (minutes.actionItems.length > 0) {
    minutes.actionItems.forEach((item) => {
      markdown += `- [ ] ${item.item} (Owner: ${item.owner}, Status: ${item.status})\n`;
    });
  } else {
    markdown += `- No action items\n`;
  }

  return markdown;
}

// Usage example
async function main() {
  const meetingId = 'YOUR_MEETING_ID';
  const accessToken = 'YOUR_ACCESS_TOKEN';

  try {
    const minutes = await generateMeetingMinutes(meetingId, accessToken);
    const markdownMinutes = formatMinutesAsMarkdown(minutes);
    console.log(markdownMinutes);
  } catch (error) {
    console.error('Failed to generate minutes:', error);
  }
}

main();
```

## Python Example

```python
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

class MeetingMinutesGenerator:
    """Generate formal meeting minutes from RTMS transcripts."""

    def __init__(self, access_token: str):
        """
        Initialize the generator with Zoom API credentials.
        
        Args:
            access_token: Zoom API access token
        """
        self.access_token = access_token
        self.base_url = "https://api.zoom.us/v2"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def generate_minutes(self, meeting_id: str) -> Dict:
        """
        Generate meeting minutes from a Zoom meeting transcript.
        
        Args:
            meeting_id: The Zoom meeting ID
            
        Returns:
            Dictionary containing structured meeting minutes
        """
        try:
            # Fetch meeting recording details
            transcript_data = self._fetch_transcript(meeting_id)
            
            # Parse and structure the transcript
            minutes = self._parse_transcript(transcript_data)
            
            return minutes
        except Exception as e:
            print(f"Error generating minutes: {str(e)}")
            raise

    def _fetch_transcript(self, meeting_id: str) -> Dict:
        """
        Fetch transcript from Zoom API.
        
        Args:
            meeting_id: The Zoom meeting ID
            
        Returns:
            Transcript data from Zoom
        """
        url = f"{self.base_url}/meetings/{meeting_id}/recordings"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        recording_data = response.json()
        
        # Find transcript file
        transcript_file = None
        for file in recording_data.get('recording_files', []):
            if file.get('file_type') == 'TRANSCRIPT':
                transcript_file = file
                break
        
        if not transcript_file:
            raise ValueError("No transcript found for this meeting")
        
        # Download transcript content
        transcript_response = requests.get(
            transcript_file['download_url'],
            headers=self.headers
        )
        transcript_response.raise_for_status()
        
        return transcript_response.json()

    def _parse_transcript(self, transcript: Dict) -> Dict:
        """
        Parse transcript and structure into meeting minutes.
        
        Args:
            transcript: Raw transcript data
            
        Returns:
            Structured meeting minutes
        """
        minutes = {
            "meeting_title": transcript.get('topic', 'Meeting Minutes'),
            "date": datetime.fromisoformat(
                transcript.get('start_time', '')
            ).strftime('%Y-%m-%d'),
            "time": datetime.fromisoformat(
                transcript.get('start_time', '')
            ).strftime('%H:%M:%S'),
            "attendees": self._extract_attendees(transcript),
            "agenda": self._extract_agenda_items(transcript),
            "decisions": self._extract_decisions(transcript),
            "action_items": self._extract_action_items(transcript),
            "next_meeting": None
        }
        
        return minutes

    def _extract_attendees(self, transcript: Dict) -> List[Dict]:
        """Extract attendees from transcript."""
        attendees = []
        speakers = set()
        
        for participant in transcript.get('participants', []):
            speakers.add(participant.get('name', 'Unknown'))
        
        for name in sorted(speakers):
            attendees.append({
                "name": name,
                "role": "Participant"
            })
        
        return attendees

    def _extract_agenda_items(self, transcript: Dict) -> List[Dict]:
        """Extract agenda items from transcript."""
        agenda_items = []
        text = transcript.get('text', '')
        sentences = [s.strip() for s in text.split(/[.!?]+/) if s.strip()]
        
        agenda_keywords = [
            'discuss', 'review', 'update', 'agenda', 'topic', 'item'
        ]
        
        for sentence in sentences:
            if any(kw in sentence.lower() for kw in agenda_keywords) and len(sentence) > 20:
                agenda_items.append({
                    "item": sentence,
                    "discussed": True
                })
        
        return agenda_items

    def _extract_decisions(self, transcript: Dict) -> List[Dict]:
        """Extract decisions from transcript."""
        decisions = []
        text = transcript.get('text', '')
        sentences = [s.strip() for s in text.split(/[.!?]+/) if s.strip()]
        
        decision_keywords = [
            'decided', 'agreed', 'approved', 'will', 'shall', 'resolved'
        ]
        
        for sentence in sentences:
            if any(kw in sentence.lower() for kw in decision_keywords) and len(sentence) > 20:
                decisions.append({
                    "decision": sentence,
                    "date": datetime.now().isoformat()
                })
        
        return decisions

    def _extract_action_items(self, transcript: Dict) -> List[Dict]:
        """Extract action items from transcript."""
        action_items = []
        text = transcript.get('text', '')
        sentences = [s.strip() for s in text.split(/[.!?]+/) if s.strip()]
        
        action_keywords = [
            'action', 'todo', 'follow up', 'send', 'prepare', 'create', 'schedule'
        ]
        
        for sentence in sentences:
            if any(kw in sentence.lower() for kw in action_keywords) and len(sentence) > 20:
                action_items.append({
                    "item": sentence,
                    "owner": "TBD",
                    "due_date": None,
                    "status": "Open"
                })
        
        return action_items

    def format_as_markdown(self, minutes: Dict) -> str:
        """
        Format meeting minutes as markdown.
        
        Args:
            minutes: Structured meeting minutes
            
        Returns:
            Formatted markdown string
        """
        markdown = f"# {minutes['meeting_title']}\n\n"
        markdown += f"**Date:** {minutes['date']}\n"
        markdown += f"**Time:** {minutes['time']}\n\n"
        
        markdown += "## Attendees\n"
        for attendee in minutes['attendees']:
            markdown += f"- {attendee['name']} ({attendee['role']})\n"
        
        markdown += "\n## Agenda\n"
        for i, item in enumerate(minutes['agenda'], 1):
            markdown += f"{i}. {item['item']}\n"
        
        markdown += "\n## Decisions\n"
        if minutes['decisions']:
            for decision in minutes['decisions']:
                markdown += f"- {decision['decision']}\n"
        else:
            markdown += "- No decisions recorded\n"
        
        markdown += "\n## Action Items\n"
        if minutes['action_items']:
            for item in minutes['action_items']:
                markdown += f"- [ ] {item['item']} (Owner: {item['owner']}, Status: {item['status']})\n"
        else:
            markdown += "- No action items\n"
        
        return markdown


# Usage example
if __name__ == "__main__":
    access_token = "YOUR_ACCESS_TOKEN"
    meeting_id = "YOUR_MEETING_ID"
    
    generator = MeetingMinutesGenerator(access_token)
    
    try:
        minutes = generator.generate_minutes(meeting_id)
        markdown_output = generator.format_as_markdown(minutes)
        print(markdown_output)
        
        # Optionally save to file
        with open("meeting_minutes.md", "w") as f:
            f.write(markdown_output)
    except Exception as e:
        print(f"Failed to generate minutes: {str(e)}")
```

## Key Features

- **Attendee Extraction**: Automatically identifies and lists all meeting participants
- **Agenda Parsing**: Extracts discussion topics from transcript text
- **Decision Capture**: Identifies and documents decisions made during the meeting
- **Action Item Tracking**: Extracts action items with owner and status tracking
- **Markdown Export**: Generates professional meeting minutes in markdown format
- **Structured Data**: Returns JSON-compatible data structures for further processing

## Implementation Notes

1. **Transcript Availability**: Ensure the meeting has been recorded and the transcript is available in Zoom
2. **API Permissions**: Requires `recording:read` scope in Zoom API credentials
3. **Keyword Matching**: The examples use simple keyword matching; consider using NLP for more sophisticated extraction
4. **Error Handling**: Both examples include error handling for API failures and missing data
5. **Customization**: Extend the extraction functions to match your specific meeting format and requirements

## Best Practices

- Validate transcript data before processing
- Handle missing or incomplete transcripts gracefully
- Store generated minutes with appropriate access controls
- Consider archiving minutes for compliance and record-keeping
- Review and edit auto-generated minutes for accuracy
