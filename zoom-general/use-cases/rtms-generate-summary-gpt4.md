# Generate Summary with GPT-4

Generate meeting summaries using OpenAI GPT-4.

## Overview

This use case demonstrates how to collect meeting transcripts from Zoom and generate intelligent summaries using OpenAI's GPT-4 Turbo model. The process involves:

1. Retrieving meeting transcripts via Zoom API
2. Processing transcript data
3. Sending to GPT-4 for summary generation
4. Storing and returning the summary

## JavaScript Example

### Prerequisites

```bash
npm install axios dotenv openai
```

### Implementation

```javascript
const axios = require('axios');
const { OpenAI } = require('openai');
require('dotenv').config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

/**
 * Fetch meeting transcript from Zoom API
 * @param {string} meetingId - Zoom meeting ID
 * @param {string} zoomAccessToken - Zoom API access token
 * @returns {Promise<string>} Meeting transcript text
 */
async function getZoomTranscript(meetingId, zoomAccessToken) {
  try {
    const response = await axios.get(
      `https://api.zoom.us/v2/meetings/${meetingId}/recordings`,
      {
        headers: {
          Authorization: `Bearer ${zoomAccessToken}`,
        },
      }
    );

    // Extract transcript from recording
    const recordings = response.data.recording_files;
    const transcriptFile = recordings.find(
      (file) => file.file_type === 'TRANSCRIPT'
    );

    if (!transcriptFile) {
      throw new Error('No transcript found for this meeting');
    }

    // Download transcript content
    const transcriptResponse = await axios.get(transcriptFile.download_url, {
      headers: {
        Authorization: `Bearer ${zoomAccessToken}`,
      },
    });

    return transcriptResponse.data;
  } catch (error) {
    console.error('Error fetching transcript:', error.message);
    throw error;
  }
}

/**
 * Generate summary using GPT-4 Turbo
 * @param {string} transcript - Meeting transcript text
 * @returns {Promise<string>} Generated summary
 */
async function generateSummaryWithGPT4(transcript) {
  try {
    const message = await openai.chat.completions.create({
      model: 'gpt-4-turbo',
      messages: [
        {
          role: 'system',
          content:
            'You are an expert meeting summarizer. Create concise, actionable summaries that capture key points, decisions, and action items.',
        },
        {
          role: 'user',
          content: `Please summarize the following meeting transcript. Include:
1. Main topics discussed
2. Key decisions made
3. Action items with owners
4. Next steps

Transcript:
${transcript}`,
        },
      ],
      temperature: 0.7,
      max_tokens: 1000,
    });

    return message.choices[0].message.content;
  } catch (error) {
    console.error('Error generating summary:', error.message);
    throw error;
  }
}

/**
 * Main function to orchestrate transcript retrieval and summary generation
 * @param {string} meetingId - Zoom meeting ID
 * @param {string} zoomAccessToken - Zoom API access token
 * @returns {Promise<Object>} Summary result with metadata
 */
async function generateMeetingSummary(meetingId, zoomAccessToken) {
  try {
    console.log(`Fetching transcript for meeting ${meetingId}...`);
    const transcript = await getZoomTranscript(meetingId, zoomAccessToken);

    console.log('Generating summary with GPT-4...');
    const summary = await generateSummaryWithGPT4(transcript);

    return {
      meetingId,
      timestamp: new Date().toISOString(),
      transcriptLength: transcript.length,
      summary,
    };
  } catch (error) {
    console.error('Failed to generate meeting summary:', error.message);
    throw error;
  }
}

// Usage
(async () => {
  const meetingId = process.env.ZOOM_MEETING_ID;
  const zoomAccessToken = process.env.ZOOM_ACCESS_TOKEN;

  const result = await generateMeetingSummary(meetingId, zoomAccessToken);
  console.log('\n=== Meeting Summary ===');
  console.log(result.summary);
})();
```

## Python Example

### Prerequisites

```bash
pip install requests python-dotenv openai
```

### Implementation

```python
import os
import requests
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def get_zoom_transcript(meeting_id: str, zoom_access_token: str) -> str:
    """
    Fetch meeting transcript from Zoom API.
    
    Args:
        meeting_id: Zoom meeting ID
        zoom_access_token: Zoom API access token
        
    Returns:
        Meeting transcript text
    """
    try:
        headers = {
            'Authorization': f'Bearer {zoom_access_token}',
        }
        
        # Get recording files
        response = requests.get(
            f'https://api.zoom.us/v2/meetings/{meeting_id}/recordings',
            headers=headers
        )
        response.raise_for_status()
        
        recordings = response.json().get('recording_files', [])
        
        # Find transcript file
        transcript_file = next(
            (f for f in recordings if f.get('file_type') == 'TRANSCRIPT'),
            None
        )
        
        if not transcript_file:
            raise ValueError('No transcript found for this meeting')
        
        # Download transcript content
        transcript_response = requests.get(
            transcript_file['download_url'],
            headers=headers
        )
        transcript_response.raise_for_status()
        
        return transcript_response.text
        
    except requests.exceptions.RequestException as e:
        print(f'Error fetching transcript: {e}')
        raise


def generate_summary_with_gpt4(transcript: str) -> str:
    """
    Generate summary using GPT-4 Turbo.
    
    Args:
        transcript: Meeting transcript text
        
    Returns:
        Generated summary
    """
    try:
        message = client.chat.completions.create(
            model='gpt-4-turbo',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are an expert meeting summarizer. Create concise, actionable summaries that capture key points, decisions, and action items.'
                },
                {
                    'role': 'user',
                    'content': f'''Please summarize the following meeting transcript. Include:
1. Main topics discussed
2. Key decisions made
3. Action items with owners
4. Next steps

Transcript:
{transcript}'''
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return message.choices[0].message.content
        
    except Exception as e:
        print(f'Error generating summary: {e}')
        raise


def generate_meeting_summary(meeting_id: str, zoom_access_token: str) -> dict:
    """
    Main function to orchestrate transcript retrieval and summary generation.
    
    Args:
        meeting_id: Zoom meeting ID
        zoom_access_token: Zoom API access token
        
    Returns:
        Dictionary with summary result and metadata
    """
    try:
        print(f'Fetching transcript for meeting {meeting_id}...')
        transcript = get_zoom_transcript(meeting_id, zoom_access_token)
        
        print('Generating summary with GPT-4...')
        summary = generate_summary_with_gpt4(transcript)
        
        return {
            'meeting_id': meeting_id,
            'timestamp': datetime.now().isoformat(),
            'transcript_length': len(transcript),
            'summary': summary
        }
        
    except Exception as e:
        print(f'Failed to generate meeting summary: {e}')
        raise


if __name__ == '__main__':
    meeting_id = os.getenv('ZOOM_MEETING_ID')
    zoom_access_token = os.getenv('ZOOM_ACCESS_TOKEN')
    
    result = generate_meeting_summary(meeting_id, zoom_access_token)
    print('\n=== Meeting Summary ===')
    print(result['summary'])
```

## Environment Variables

Create a `.env` file with the following variables:

```
ZOOM_MEETING_ID=your_meeting_id
ZOOM_ACCESS_TOKEN=your_zoom_api_token
OPENAI_API_KEY=your_openai_api_key
```

## API Requirements

### Zoom API
- **Endpoint**: `GET /v2/meetings/{meetingId}/recordings`
- **Scopes**: `recording:read`
- **Authentication**: OAuth 2.0 Bearer Token

### OpenAI API
- **Model**: `gpt-4-turbo`
- **Authentication**: API Key

## Response Format

Both examples return a structured response:

```json
{
  "meetingId": "123456789",
  "timestamp": "2024-01-27T10:30:00Z",
  "transcriptLength": 5000,
  "summary": "Meeting focused on Q1 planning. Key decisions: adopt new development framework, allocate 2 engineers to infrastructure. Action items: John to prepare migration plan by Feb 1, Sarah to conduct team training by Feb 15."
}
```

## Error Handling

Both implementations include error handling for:
- Missing or invalid meeting IDs
- API authentication failures
- Network timeouts
- Missing transcript files
- OpenAI API errors

## Best Practices

1. **Rate Limiting**: Implement exponential backoff for API calls
2. **Caching**: Store summaries to avoid regenerating for the same meeting
3. **Transcript Validation**: Verify transcript quality before sending to GPT-4
4. **Token Management**: Monitor OpenAI token usage for cost optimization
5. **Async Processing**: Use job queues for large-scale summary generation

## Limitations

- Transcript availability depends on Zoom recording settings
- GPT-4 Turbo has token limits (128K context window)
- Very long meetings may need to be chunked
- Summary quality depends on transcript clarity

## See Also

- [Zoom Recording API Documentation](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/getRecordings)
- [OpenAI GPT-4 Documentation](https://platform.openai.com/docs/models/gpt-4-turbo)
- [Zoom OAuth 2.0 Authentication](https://developers.zoom.us/docs/internal-apps/oauth/)
