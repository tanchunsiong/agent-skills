# Generate Summary with Claude

Generate meeting summaries using Anthropic Claude's powerful language models to automatically create concise, actionable summaries from Zoom meeting transcripts.

## Overview

This use case demonstrates how to integrate Anthropic's Claude API with Zoom's Real-Time Messaging Service (RTMS) to generate intelligent meeting summaries. Claude can analyze meeting transcripts and produce summaries that capture key points, decisions, and action items.

## Prerequisites

- Zoom account with RTMS access
- Anthropic API key
- Node.js (for JavaScript examples) or Python 3.8+ (for Python examples)
- Required dependencies installed

## JavaScript Example

### Installation

```bash
npm install @anthropic-ai/sdk axios
```

### Code

```javascript
const Anthropic = require("@anthropic-ai/sdk");

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function generateMeetingSummary(transcript) {
  const message = await client.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: `Please analyze the following meeting transcript and provide a comprehensive summary that includes:
1. Main topics discussed
2. Key decisions made
3. Action items with owners
4. Next steps

Meeting Transcript:
${transcript}

Please format the summary in a clear, structured manner.`,
      },
    ],
  });

  return message.content[0].text;
}

async function main() {
  const sampleTranscript = `
    John: Good morning everyone. Let's discuss the Q1 product roadmap.
    Sarah: I think we should prioritize the mobile app improvements.
    John: Agreed. Sarah, can you lead that initiative?
    Sarah: Yes, I'll start working on the requirements this week.
    Mike: What about the API performance issues?
    John: Good point. Mike, can you investigate and report back by Friday?
    Mike: Sure, I'll have a report ready.
    Sarah: We should also schedule a follow-up meeting next week.
    John: Perfect. Let's reconvene on Tuesday at 2 PM.
  `;

  try {
    console.log("Generating meeting summary...\n");
    const summary = await generateMeetingSummary(sampleTranscript);
    console.log("Meeting Summary:\n");
    console.log(summary);
  } catch (error) {
    console.error("Error generating summary:", error);
    process.exit(1);
  }
}

main();
```

### Usage

```bash
export ANTHROPIC_API_KEY=your_api_key_here
node generate-summary.js
```

## Python Example

### Installation

```bash
pip install anthropic
```

### Code

```python
import anthropic
import os


def generate_meeting_summary(transcript: str) -> str:
    """Generate a meeting summary using Claude."""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Please analyze the following meeting transcript and provide a comprehensive summary that includes:
1. Main topics discussed
2. Key decisions made
3. Action items with owners
4. Next steps

Meeting Transcript:
{transcript}

Please format the summary in a clear, structured manner.""",
            }
        ],
    )

    return message.content[0].text


def main():
    sample_transcript = """
    John: Good morning everyone. Let's discuss the Q1 product roadmap.
    Sarah: I think we should prioritize the mobile app improvements.
    John: Agreed. Sarah, can you lead that initiative?
    Sarah: Yes, I'll start working on the requirements this week.
    Mike: What about the API performance issues?
    John: Good point. Mike, can you investigate and report back by Friday?
    Mike: Sure, I'll have a report ready.
    Sarah: We should also schedule a follow-up meeting next week.
    John: Perfect. Let's reconvene on Tuesday at 2 PM.
    """

    try:
        print("Generating meeting summary...\n")
        summary = generate_meeting_summary(sample_transcript)
        print("Meeting Summary:\n")
        print(summary)
    except anthropic.APIError as e:
        print(f"Error generating summary: {e}")
        exit(1)


if __name__ == "__main__":
    main()
```

### Usage

```bash
export ANTHROPIC_API_KEY=your_api_key_here
python generate_summary.py
```

## Integration with Zoom RTMS

To integrate this with Zoom's Real-Time Messaging Service:

1. **Capture Transcript**: Use Zoom's RTMS API to capture meeting transcripts in real-time or retrieve them after the meeting
2. **Process with Claude**: Send the transcript to Claude for summarization
3. **Store Results**: Save the generated summary to your database or send it to meeting participants
4. **Enhance**: Add custom prompts for specific meeting types (standup, planning, retrospective, etc.)

## Advanced Features

### Custom Summarization Prompts

Tailor summaries for different meeting types:

```javascript
const meetingTypePrompts = {
  standup: "Focus on blockers, completed tasks, and planned work",
  planning: "Highlight goals, timelines, and resource allocation",
  retrospective: "Emphasize lessons learned and action items for improvement",
  client: "Summarize deliverables, timelines, and client feedback",
};
```

### Multi-Language Support

Claude supports summarization in multiple languages. Specify the desired language in your prompt:

```javascript
const message = await client.messages.create({
  model: "claude-3-5-sonnet-20241022",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: `Summarize this meeting transcript in Spanish: ${transcript}`,
    },
  ],
});
```

## Best Practices

1. **Transcript Quality**: Ensure transcripts are accurate and properly formatted
2. **Token Management**: Monitor API usage for long transcripts; consider chunking if needed
3. **Prompt Engineering**: Customize prompts for your specific use case and meeting types
4. **Error Handling**: Implement robust error handling for API failures
5. **Privacy**: Ensure sensitive information is handled securely and complies with regulations

## Troubleshooting

- **API Rate Limits**: Implement exponential backoff for retries
- **Long Transcripts**: Split very long transcripts into sections and summarize each part
- **Quality Issues**: Refine prompts and provide examples for better results
- **Cost Optimization**: Use Claude 3 Haiku for faster, more cost-effective summarization of simple transcripts

## Resources

- [Anthropic Claude API Documentation](https://docs.anthropic.com)
- [Zoom RTMS Documentation](https://developers.zoom.us)
- [Claude Models Overview](https://docs.anthropic.com/claude/reference/models-overview)

## Support

For issues or questions:
- Check the Anthropic documentation
- Review Zoom's developer resources
- Consult the Claude API reference guide
