# Anthropic Claude Integration

## Brief
Integrate RTMS transcripts with Anthropic Claude for meeting analysis.

## Overview
This use case demonstrates how to leverage Anthropic's Claude API to analyze Zoom meeting transcripts obtained through the Real-Time Messaging Service (RTMS). Claude can extract insights, summarize discussions, identify action items, and provide intelligent analysis of meeting content.

## Use Cases
- **Meeting Summarization**: Generate concise summaries of long meetings
- **Action Item Extraction**: Identify and list action items with owners
- **Sentiment Analysis**: Analyze meeting tone and participant sentiment
- **Key Topic Identification**: Extract main discussion topics
- **Decision Documentation**: Capture decisions made during meetings

## JavaScript Implementation

### Installation
```bash
npm install @anthropic-ai/sdk
```

### Basic Example: Meeting Summary
```javascript
const Anthropic = require("@anthropic-ai/sdk");

const client = new Anthropic();

async function analyzeMeetingTranscript(transcript) {
  const message = await client.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: `Please analyze the following meeting transcript and provide:
1. A brief summary (2-3 sentences)
2. Key discussion points (bullet list)
3. Action items with owners
4. Decisions made

Transcript:
${transcript}`,
      },
    ],
  });

  return message.content[0].type === "text" ? message.content[0].text : null;
}

// Example usage
const sampleTranscript = `
John: Good morning everyone. Let's discuss the Q1 roadmap.
Sarah: I think we should prioritize the API improvements.
John: Agreed. Sarah, can you lead that initiative?
Sarah: Yes, I'll start next week.
Mike: What about the dashboard redesign?
John: Let's schedule that for Q2. Mike, can you prepare a proposal?
Mike: Sure, I'll have it ready by Friday.
`;

analyzeMeetingTranscript(sampleTranscript)
  .then((analysis) => console.log(analysis))
  .catch((error) => console.error(error));
```

### Advanced Example: Structured Analysis
```javascript
const Anthropic = require("@anthropic-ai/sdk");

const client = new Anthropic();

async function structuredMeetingAnalysis(transcript) {
  const message = await client.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 2048,
    messages: [
      {
        role: "user",
        content: `Analyze this meeting transcript and return a JSON object with the following structure:
{
  "summary": "brief summary",
  "participants": ["list of participants"],
  "topics": ["main topics discussed"],
  "actionItems": [
    {
      "task": "description",
      "owner": "person responsible",
      "dueDate": "estimated due date if mentioned"
    }
  ],
  "decisions": ["decisions made"],
  "sentiment": "overall tone (positive/neutral/negative)"
}

Transcript:
${transcript}`,
      },
    ],
  });

  const responseText =
    message.content[0].type === "text" ? message.content[0].text : "";

  // Extract JSON from response
  const jsonMatch = responseText.match(/\{[\s\S]*\}/);
  return jsonMatch ? JSON.parse(jsonMatch[0]) : null;
}

// Example usage
const transcript = `
Alice: Welcome to the product planning meeting.
Bob: Thanks for organizing this. I wanted to discuss the mobile app performance issues.
Alice: Good point. What specific issues are you seeing?
Bob: Users report slow load times on Android devices. I think we need to optimize the API calls.
Carol: I agree. I can help with the backend optimization. I'll start investigating this week.
Bob: Great! Can you also check the database queries?
Carol: Yes, that's on my list. I'll have a report by next Friday.
Alice: Excellent. Let's also plan for the iOS update. Bob, can you coordinate with the iOS team?
Bob: Absolutely. I'll schedule a meeting with them tomorrow.
Alice: Perfect. Let's reconvene next week to review progress.
`;

structuredMeetingAnalysis(transcript)
  .then((analysis) => console.log(JSON.stringify(analysis, null, 2)))
  .catch((error) => console.error(error));
```

## Python Implementation

### Installation
```bash
pip install anthropic
```

### Basic Example: Meeting Summary
```python
from anthropic import Anthropic

client = Anthropic()

def analyze_meeting_transcript(transcript):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Please analyze the following meeting transcript and provide:
1. A brief summary (2-3 sentences)
2. Key discussion points (bullet list)
3. Action items with owners
4. Decisions made

Transcript:
{transcript}""",
            }
        ],
    )

    return message.content[0].text if message.content[0].type == "text" else None


# Example usage
sample_transcript = """
John: Good morning everyone. Let's discuss the Q1 roadmap.
Sarah: I think we should prioritize the API improvements.
John: Agreed. Sarah, can you lead that initiative?
Sarah: Yes, I'll start next week.
Mike: What about the dashboard redesign?
John: Let's schedule that for Q2. Mike, can you prepare a proposal?
Mike: Sure, I'll have it ready by Friday.
"""

analysis = analyze_meeting_transcript(sample_transcript)
print(analysis)
```

### Advanced Example: Structured Analysis
```python
import json
from anthropic import Anthropic

client = Anthropic()

def structured_meeting_analysis(transcript):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"""Analyze this meeting transcript and return a JSON object with the following structure:
{{
  "summary": "brief summary",
  "participants": ["list of participants"],
  "topics": ["main topics discussed"],
  "actionItems": [
    {{
      "task": "description",
      "owner": "person responsible",
      "dueDate": "estimated due date if mentioned"
    }}
  ],
  "decisions": ["decisions made"],
  "sentiment": "overall tone (positive/neutral/negative)"
}}

Transcript:
{transcript}""",
            }
        ],
    )

    response_text = message.content[0].text if message.content[0].type == "text" else ""

    # Extract JSON from response
    try:
        start_idx = response_text.find("{")
        end_idx = response_text.rfind("}") + 1
        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass

    return None


# Example usage
transcript = """
Alice: Welcome to the product planning meeting.
Bob: Thanks for organizing this. I wanted to discuss the mobile app performance issues.
Alice: Good point. What specific issues are you seeing?
Bob: Users report slow load times on Android devices. I think we need to optimize the API calls.
Carol: I agree. I can help with the backend optimization. I'll start investigating this week.
Bob: Great! Can you also check the database queries?
Carol: Yes, that's on my list. I'll have a report by next Friday.
Alice: Excellent. Let's also plan for the iOS update. Bob, can you coordinate with the iOS team?
Bob: Absolutely. I'll schedule a meeting with them tomorrow.
Alice: Perfect. Let's reconvene next week to review progress.
"""

analysis = structured_meeting_analysis(transcript)
if analysis:
    print(json.dumps(analysis, indent=2))
```

## Integration with RTMS

### Workflow
1. **Capture Transcript**: Use Zoom RTMS to capture real-time meeting transcript
2. **Process Transcript**: Clean and format the transcript data
3. **Send to Claude**: Use the Messages API to analyze the transcript
4. **Store Results**: Save analysis results to your database
5. **Display Insights**: Present insights in your application UI

### Example: RTMS to Claude Pipeline (JavaScript)
```javascript
const Anthropic = require("@anthropic-ai/sdk");

const client = new Anthropic();

async function processRTMSTranscript(rtmsData) {
  // rtmsData contains: { meetingId, participants, transcript, timestamp }

  // Format transcript from RTMS
  const formattedTranscript = rtmsData.transcript
    .map((entry) => `${entry.speaker}: ${entry.text}`)
    .join("\n");

  // Analyze with Claude
  const message = await client.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 2048,
    messages: [
      {
        role: "user",
        content: `Analyze this meeting transcript from meeting ID ${rtmsData.meetingId}:

${formattedTranscript}

Provide a comprehensive analysis including summary, action items, and key decisions.`,
      },
    ],
  });

  return {
    meetingId: rtmsData.meetingId,
    timestamp: rtmsData.timestamp,
    analysis: message.content[0].text,
  };
}
```

## Best Practices

1. **Transcript Formatting**: Clean up speaker names and timestamps for clarity
2. **Token Management**: Monitor token usage for long transcripts; consider chunking
3. **Error Handling**: Implement retry logic for API failures
4. **Privacy**: Ensure sensitive information is handled appropriately
5. **Caching**: Cache analysis results to avoid redundant API calls
6. **Model Selection**: Use appropriate Claude model based on complexity needs

## API Reference

### Messages API Endpoint
- **Endpoint**: `POST https://api.anthropic.com/v1/messages`
- **Authentication**: Bearer token in Authorization header
- **Required Parameters**:
  - `model`: Claude model ID (e.g., "claude-3-5-sonnet-20241022")
  - `max_tokens`: Maximum tokens in response
  - `messages`: Array of message objects with role and content

### Supported Models
- `claude-3-5-sonnet-20241022`: Latest Sonnet model (recommended for most use cases)
- `claude-3-opus-20250219`: Most capable model for complex analysis
- `claude-3-haiku-20250307`: Fastest model for simple tasks

## Resources

- [Anthropic API Documentation](https://docs.anthropic.com)
- [Claude Models](https://docs.anthropic.com/en/docs/about-claude/models/latest)
- [Messages API Guide](https://docs.anthropic.com/en/docs/build-a-chatbot-with-claude)
- [Zoom RTMS Documentation](https://developers.zoom.us/docs/meeting-sdk/web/rtms/)
