# OpenAI Integration

## Brief

Integrate RTMS transcripts with OpenAI GPT models for real-time meeting intelligence. Analyze meeting transcripts in real-time to extract insights, generate summaries, identify action items, and provide intelligent meeting assistance.

## Overview

This use case demonstrates how to connect Zoom's Real-Time Messaging Service (RTMS) with OpenAI's GPT models to provide intelligent analysis of meeting transcripts as they happen. By streaming transcript data to OpenAI's Chat Completions API, you can generate real-time insights, summaries, and actionable intelligence during or immediately after meetings.

## Use Cases

- **Real-time Meeting Summaries**: Generate automatic summaries as the meeting progresses
- **Action Item Extraction**: Identify and track action items and decisions in real-time
- **Sentiment Analysis**: Analyze meeting tone and participant sentiment
- **Key Topic Identification**: Extract and highlight important discussion topics
- **Meeting Intelligence**: Provide AI-powered insights and recommendations
- **Transcript Enhancement**: Add context, clarifications, and structured data to raw transcripts

## JavaScript Implementation

### Prerequisites

```bash
npm install openai
```

### Basic Setup

```javascript
const OpenAI = require('openai');

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});
```

### Real-Time Transcript Analysis

```javascript
const OpenAI = require('openai');

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

/**
 * Analyze a meeting transcript using OpenAI Chat Completions
 * @param {string} transcript - The meeting transcript text
 * @returns {Promise<string>} - Analysis result from OpenAI
 */
async function analyzeTranscript(transcript) {
  try {
    const message = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'You are an expert meeting analyst. Analyze the provided meeting transcript and provide insights.',
        },
        {
          role: 'user',
          content: `Please analyze this meeting transcript and provide:
1. A brief summary (2-3 sentences)
2. Key topics discussed
3. Action items identified
4. Decisions made
5. Overall sentiment

Transcript:
${transcript}`,
        },
      ],
      temperature: 0.7,
      max_tokens: 1000,
    });

    return message.choices[0].message.content;
  } catch (error) {
    console.error('Error analyzing transcript:', error);
    throw error;
  }
}

/**
 * Extract action items from a transcript
 * @param {string} transcript - The meeting transcript text
 * @returns {Promise<Array>} - Array of action items
 */
async function extractActionItems(transcript) {
  try {
    const message = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'You are an expert at identifying action items from meeting transcripts. Extract all action items with assigned owners and due dates.',
        },
        {
          role: 'user',
          content: `Extract all action items from this transcript. Format as JSON array with fields: task, owner, dueDate, priority.

Transcript:
${transcript}`,
        },
      ],
      temperature: 0.5,
      max_tokens: 800,
    });

    const content = message.choices[0].message.content;
    // Parse JSON from response
    const jsonMatch = content.match(/\[[\s\S]*\]/);
    return jsonMatch ? JSON.parse(jsonMatch[0]) : [];
  } catch (error) {
    console.error('Error extracting action items:', error);
    throw error;
  }
}

/**
 * Stream real-time analysis as transcript is being generated
 * @param {string} transcript - The meeting transcript text
 * @param {Function} onChunk - Callback for each streamed chunk
 */
async function streamTranscriptAnalysis(transcript, onChunk) {
  try {
    const stream = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'You are an expert meeting analyst providing real-time insights.',
        },
        {
          role: 'user',
          content: `Analyze this meeting transcript in real-time:

${transcript}

Provide insights on key topics, decisions, and action items.`,
        },
      ],
      temperature: 0.7,
      max_tokens: 1500,
      stream: true,
    });

    for await (const chunk of stream) {
      if (chunk.choices[0].delta.content) {
        onChunk(chunk.choices[0].delta.content);
      }
    }
  } catch (error) {
    console.error('Error streaming analysis:', error);
    throw error;
  }
}

/**
 * Generate a meeting summary with specific focus areas
 * @param {string} transcript - The meeting transcript text
 * @param {Array<string>} focusAreas - Areas to focus on in the summary
 * @returns {Promise<Object>} - Structured summary
 */
async function generateStructuredSummary(transcript, focusAreas = []) {
  try {
    const focusPrompt = focusAreas.length > 0 
      ? `Focus on these areas: ${focusAreas.join(', ')}`
      : '';

    const message = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'You are an expert meeting summarizer. Provide structured, actionable summaries.',
        },
        {
          role: 'user',
          content: `Generate a structured summary of this meeting transcript. ${focusPrompt}

Return as JSON with fields: summary, keyTopics, decisions, actionItems, risks, nextSteps.

Transcript:
${transcript}`,
        },
      ],
      temperature: 0.6,
      max_tokens: 1200,
    });

    const content = message.choices[0].message.content;
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    return jsonMatch ? JSON.parse(jsonMatch[0]) : { summary: content };
  } catch (error) {
    console.error('Error generating summary:', error);
    throw error;
  }
}

// Example usage
async function main() {
  const sampleTranscript = `
    John: Good morning everyone. Let's discuss the Q1 product roadmap.
    Sarah: I think we should prioritize the API improvements. We've had several customer requests.
    John: Agreed. Sarah, can you lead that initiative?
    Sarah: Yes, I'll start next week. I'll need 2 engineers.
    Mike: I can assign Tom and Lisa to help.
    John: Great. We also need to fix the authentication issues. Mike, can you handle that?
    Mike: Sure, I'll create a task and assign it to the team. Target is end of February.
    Sarah: What about the mobile app redesign?
    John: Let's push that to Q2. We need to focus on stability first.
    All: Sounds good.
  `;

  console.log('Analyzing transcript...\n');
  const analysis = await analyzeTranscript(sampleTranscript);
  console.log('Analysis:\n', analysis);

  console.log('\n\nExtracting action items...\n');
  const actionItems = await extractActionItems(sampleTranscript);
  console.log('Action Items:\n', JSON.stringify(actionItems, null, 2));

  console.log('\n\nGenerating structured summary...\n');
  const summary = await generateStructuredSummary(sampleTranscript, ['decisions', 'action items']);
  console.log('Summary:\n', JSON.stringify(summary, null, 2));

  console.log('\n\nStreaming real-time analysis...\n');
  await streamTranscriptAnalysis(sampleTranscript, (chunk) => {
    process.stdout.write(chunk);
  });
}

main().catch(console.error);
```

## Python Implementation

### Prerequisites

```bash
pip install openai
```

### Basic Setup

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")
```

### Real-Time Transcript Analysis

```python
from openai import OpenAI
import json

client = OpenAI()

def analyze_transcript(transcript: str) -> str:
    """
    Analyze a meeting transcript using OpenAI Chat Completions.
    
    Args:
        transcript: The meeting transcript text
        
    Returns:
        Analysis result from OpenAI
    """
    try:
        message = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert meeting analyst. Analyze the provided meeting transcript and provide insights."
                },
                {
                    "role": "user",
                    "content": f"""Please analyze this meeting transcript and provide:
1. A brief summary (2-3 sentences)
2. Key topics discussed
3. Action items identified
4. Decisions made
5. Overall sentiment

Transcript:
{transcript}"""
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return message.choices[0].message.content
    except Exception as e:
        print(f"Error analyzing transcript: {e}")
        raise


def extract_action_items(transcript: str) -> list:
    """
    Extract action items from a transcript.
    
    Args:
        transcript: The meeting transcript text
        
    Returns:
        List of action items with details
    """
    try:
        message = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at identifying action items from meeting transcripts. Extract all action items with assigned owners and due dates."
                },
                {
                    "role": "user",
                    "content": f"""Extract all action items from this transcript. Format as JSON array with fields: task, owner, dueDate, priority.

Transcript:
{transcript}"""
                }
            ],
            temperature=0.5,
            max_tokens=800
        )
        
        content = message.choices[0].message.content
        # Parse JSON from response
        try:
            # Find JSON array in response
            start = content.find('[')
            end = content.rfind(']') + 1
            if start != -1 and end > start:
                return json.loads(content[start:end])
        except json.JSONDecodeError:
            pass
        
        return []
    except Exception as e:
        print(f"Error extracting action items: {e}")
        raise


def stream_transcript_analysis(transcript: str, on_chunk=None):
    """
    Stream real-time analysis as transcript is being generated.
    
    Args:
        transcript: The meeting transcript text
        on_chunk: Callback function for each streamed chunk
    """
    try:
        with client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert meeting analyst providing real-time insights."
                },
                {
                    "role": "user",
                    "content": f"""Analyze this meeting transcript in real-time:

{transcript}

Provide insights on key topics, decisions, and action items."""
                }
            ],
            temperature=0.7,
            max_tokens=1500,
            stream=True
        ) as stream:
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    if on_chunk:
                        on_chunk(content)
                    else:
                        print(content, end='', flush=True)
    except Exception as e:
        print(f"Error streaming analysis: {e}")
        raise


def generate_structured_summary(transcript: str, focus_areas: list = None) -> dict:
    """
    Generate a meeting summary with specific focus areas.
    
    Args:
        transcript: The meeting transcript text
        focus_areas: List of areas to focus on in the summary
        
    Returns:
        Structured summary as dictionary
    """
    try:
        focus_prompt = f"Focus on these areas: {', '.join(focus_areas)}" if focus_areas else ""
        
        message = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert meeting summarizer. Provide structured, actionable summaries."
                },
                {
                    "role": "user",
                    "content": f"""Generate a structured summary of this meeting transcript. {focus_prompt}

Return as JSON with fields: summary, keyTopics, decisions, actionItems, risks, nextSteps.

Transcript:
{transcript}"""
                }
            ],
            temperature=0.6,
            max_tokens=1200
        )
        
        content = message.choices[0].message.content
        try:
            # Find JSON object in response
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(content[start:end])
        except json.JSONDecodeError:
            pass
        
        return {"summary": content}
    except Exception as e:
        print(f"Error generating summary: {e}")
        raise


def main():
    sample_transcript = """
    John: Good morning everyone. Let's discuss the Q1 product roadmap.
    Sarah: I think we should prioritize the API improvements. We've had several customer requests.
    John: Agreed. Sarah, can you lead that initiative?
    Sarah: Yes, I'll start next week. I'll need 2 engineers.
    Mike: I can assign Tom and Lisa to help.
    John: Great. We also need to fix the authentication issues. Mike, can you handle that?
    Mike: Sure, I'll create a task and assign it to the team. Target is end of February.
    Sarah: What about the mobile app redesign?
    John: Let's push that to Q2. We need to focus on stability first.
    All: Sounds good.
    """
    
    print("Analyzing transcript...\n")
    analysis = analyze_transcript(sample_transcript)
    print("Analysis:\n", analysis)
    
    print("\n\nExtracting action items...\n")
    action_items = extract_action_items(sample_transcript)
    print("Action Items:\n", json.dumps(action_items, indent=2))
    
    print("\n\nGenerating structured summary...\n")
    summary = generate_structured_summary(sample_transcript, focus_areas=["decisions", "action items"])
    print("Summary:\n", json.dumps(summary, indent=2))
    
    print("\n\nStreaming real-time analysis...\n")
    stream_transcript_analysis(sample_transcript)


if __name__ == "__main__":
    main()
```

## Integration with RTMS

### JavaScript RTMS Integration

```javascript
const OpenAI = require('openai');
const { RTMSClient } = require('@zoom/rtms-client');

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

class RTMSOpenAIIntegration {
  constructor(rtmsConfig) {
    this.rtmsClient = new RTMSClient(rtmsConfig);
    this.transcriptBuffer = '';
    this.analysisInterval = 30000; // Analyze every 30 seconds
  }

  async connect() {
    this.rtmsClient.on('transcript', (data) => {
      this.transcriptBuffer += data.text + ' ';
      
      // Trigger analysis periodically
      if (!this.analysisTimer) {
        this.analysisTimer = setInterval(() => {
          this.analyzeBuffer();
        }, this.analysisInterval);
      }
    });

    await this.rtmsClient.connect();
  }

  async analyzeBuffer() {
    if (this.transcriptBuffer.trim().length === 0) return;

    try {
      const message = await openai.chat.completions.create({
        model: 'gpt-4',
        messages: [
          {
            role: 'system',
            content: 'Provide real-time meeting insights from the transcript excerpt.',
          },
          {
            role: 'user',
            content: `Analyze this meeting excerpt:\n${this.transcriptBuffer}`,
          },
        ],
        temperature: 0.7,
        max_tokens: 500,
      });

      console.log('Real-time Insight:', message.choices[0].message.content);
      this.transcriptBuffer = ''; // Clear buffer after analysis
    } catch (error) {
      console.error('Analysis error:', error);
    }
  }

  disconnect() {
    if (this.analysisTimer) {
      clearInterval(this.analysisTimer);
    }
    this.rtmsClient.disconnect();
  }
}

module.exports = RTMSOpenAIIntegration;
```

### Python RTMS Integration

```python
from openai import OpenAI
from zoom_rtms import RTMSClient
import asyncio
import threading

client = OpenAI()

class RTMSOpenAIIntegration:
    def __init__(self, rtms_config):
        self.rtms_client = RTMSClient(rtms_config)
        self.transcript_buffer = ""
        self.analysis_interval = 30  # Analyze every 30 seconds
        self.analysis_thread = None
        
    async def connect(self):
        """Connect to RTMS and start listening for transcripts."""
        self.rtms_client.on_transcript(self._on_transcript)
        await self.rtms_client.connect()
        
        # Start analysis thread
        self.analysis_thread = threading.Thread(
            target=self._analysis_loop,
            daemon=True
        )
        self.analysis_thread.start()
    
    def _on_transcript(self, data):
        """Handle incoming transcript data."""
        self.transcript_buffer += data.get('text', '') + ' '
    
    def _analysis_loop(self):
        """Periodically analyze transcript buffer."""
        while True:
            asyncio.sleep(self.analysis_interval)
            if self.transcript_buffer.strip():
                self._analyze_buffer()
    
    def _analyze_buffer(self):
        """Analyze current transcript buffer."""
        try:
            message = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Provide real-time meeting insights from the transcript excerpt."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this meeting excerpt:\n{self.transcript_buffer}"
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            print("Real-time Insight:", message.choices[0].message.content)
            self.transcript_buffer = ""  # Clear buffer after analysis
        except Exception as e:
            print(f"Analysis error: {e}")
    
    async def disconnect(self):
        """Disconnect from RTMS."""
        await self.rtms_client.disconnect()
```

## Best Practices

1. **Rate Limiting**: Implement rate limiting to avoid exceeding OpenAI API quotas
2. **Error Handling**: Always wrap API calls in try-catch blocks
3. **Streaming**: Use streaming for real-time analysis to reduce latency
4. **Caching**: Cache analysis results to avoid duplicate API calls
5. **Privacy**: Ensure transcripts are handled securely and comply with privacy regulations
6. **Token Management**: Monitor token usage to manage costs
7. **Prompt Engineering**: Craft specific prompts for better analysis results
8. **Async Processing**: Use async/await for non-blocking operations

## Security Considerations

- Store API keys in environment variables, never in code
- Implement proper authentication for RTMS connections
- Encrypt transcript data in transit and at rest
- Implement access controls for analysis results
- Log API usage for audit purposes
- Comply with data retention policies

## References

- [OpenAI Chat Completions API](https://platform.openai.com/docs/api-reference/chat/create)
- [OpenAI Node.js Library](https://github.com/openai/node-sdk)
- [OpenAI Python Library](https://github.com/openai/openai-python)
- [Zoom RTMS Documentation](https://developers.zoom.us/docs/rtms/)
