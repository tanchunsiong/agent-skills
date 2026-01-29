# LangChain Integration

## Brief

Use LangChain for meeting analysis with RTMS transcripts. Leverage LangChain's chain abstractions to build intelligent meeting analysis pipelines that extract insights, summarize discussions, and identify action items from Zoom meeting transcripts.

## Overview

This guide demonstrates how to integrate LangChain with Zoom's Real-Time Messaging Service (RTMS) transcripts to create powerful meeting intelligence applications. LangChain provides composable abstractions for building chains that process meeting data through language models.

## JavaScript/TypeScript Example

### Installation

```bash
npm install langchain @langchain/openai dotenv
```

### Basic Meeting Analysis Chain

```javascript
import { OpenAI } from "@langchain/openai";
import { PromptTemplate } from "@langchain/core/prompts";
import { LLMChain } from "langchain/chains";

// Initialize the LLM
const llm = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  temperature: 0.7,
});

// Define a prompt template for meeting analysis
const meetingAnalysisPrompt = new PromptTemplate({
  inputVariables: ["transcript"],
  template: `Analyze the following meeting transcript and provide:
1. Key discussion points
2. Action items with owners
3. Decisions made
4. Next steps

Transcript:
{transcript}

Analysis:`,
});

// Create the chain
const analysisChain = new LLMChain({
  llm,
  prompt: meetingAnalysisPrompt,
});

// Use the chain
async function analyzeMeeting(transcript) {
  const result = await analysisChain.call({
    transcript: transcript,
  });
  return result.text;
}

// Example usage
const sampleTranscript = `
John: Let's discuss the Q1 roadmap.
Sarah: We should prioritize the API improvements.
John: Agreed. Sarah, can you lead that initiative?
Sarah: Yes, I'll start next week.
John: Great. Let's also schedule a follow-up for next Friday.
`;

analyzeMeeting(sampleTranscript).then((analysis) => {
  console.log("Meeting Analysis:\n", analysis);
});
```

### Advanced Chain with Sequential Processing

```javascript
import { SequentialChain } from "langchain/chains";
import { PromptTemplate } from "@langchain/core/prompts";
import { OpenAI } from "@langchain/openai";

const llm = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  temperature: 0.7,
});

// Chain 1: Summarize the meeting
const summaryPrompt = new PromptTemplate({
  inputVariables: ["transcript"],
  template: `Summarize this meeting transcript in 2-3 sentences:
{transcript}

Summary:`,
});

const summaryChain = new LLMChain({
  llm,
  prompt: summaryPrompt,
  outputKey: "summary",
});

// Chain 2: Extract action items
const actionItemsPrompt = new PromptTemplate({
  inputVariables: ["transcript"],
  template: `Extract all action items from this transcript. Format as a numbered list with owner:
{transcript}

Action Items:`,
});

const actionItemsChain = new LLMChain({
  llm,
  prompt: actionItemsPrompt,
  outputKey: "actionItems",
});

// Chain 3: Identify decisions
const decisionsPrompt = new PromptTemplate({
  inputVariables: ["transcript"],
  template: `List all decisions made in this meeting:
{transcript}

Decisions:`,
});

const decisionsChain = new LLMChain({
  llm,
  prompt: decisionsPrompt,
  outputKey: "decisions",
});

// Combine chains sequentially
const overallChain = new SequentialChain({
  chains: [summaryChain, actionItemsChain, decisionsChain],
  inputVariables: ["transcript"],
  outputVariables: ["summary", "actionItems", "decisions"],
});

// Execute the chain
async function processTranscript(transcript) {
  const result = await overallChain.call({
    transcript: transcript,
  });
  return result;
}
```

## Python Example

### Installation

```bash
pip install langchain openai python-dotenv
```

### Basic Meeting Analysis Chain

```python
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# Initialize the LLM
llm = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

# Define a prompt template for meeting analysis
meeting_analysis_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="""Analyze the following meeting transcript and provide:
1. Key discussion points
2. Action items with owners
3. Decisions made
4. Next steps

Transcript:
{transcript}

Analysis:"""
)

# Create the chain
analysis_chain = LLMChain(
    llm=llm,
    prompt=meeting_analysis_prompt
)

# Use the chain
def analyze_meeting(transcript):
    result = analysis_chain.run(transcript=transcript)
    return result

# Example usage
sample_transcript = """
John: Let's discuss the Q1 roadmap.
Sarah: We should prioritize the API improvements.
John: Agreed. Sarah, can you lead that initiative?
Sarah: Yes, I'll start next week.
John: Great. Let's also schedule a follow-up for next Friday.
"""

analysis = analyze_meeting(sample_transcript)
print("Meeting Analysis:\n", analysis)
```

### Advanced Chain with Sequential Processing

```python
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
import os

llm = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

# Chain 1: Summarize the meeting
summary_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="""Summarize this meeting transcript in 2-3 sentences:
{transcript}

Summary:"""
)

summary_chain = LLMChain(
    llm=llm,
    prompt=summary_prompt,
    output_key="summary"
)

# Chain 2: Extract action items
action_items_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="""Extract all action items from this transcript. Format as a numbered list with owner:
{transcript}

Action Items:"""
)

action_items_chain = LLMChain(
    llm=llm,
    prompt=action_items_prompt,
    output_key="action_items"
)

# Chain 3: Identify decisions
decisions_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="""List all decisions made in this meeting:
{transcript}

Decisions:"""
)

decisions_chain = LLMChain(
    llm=llm,
    prompt=decisions_prompt,
    output_key="decisions"
)

# Combine chains sequentially
overall_chain = SequentialChain(
    chains=[summary_chain, action_items_chain, decisions_chain],
    input_variables=["transcript"],
    output_variables=["summary", "action_items", "decisions"],
    verbose=True
)

# Execute the chain
def process_transcript(transcript):
    result = overall_chain({"transcript": transcript})
    return result

# Example usage
sample_transcript = """
John: Let's discuss the Q1 roadmap.
Sarah: We should prioritize the API improvements.
John: Agreed. Sarah, can you lead that initiative?
Sarah: Yes, I'll start next week.
John: Great. Let's also schedule a follow-up for next Friday.
"""

result = process_transcript(sample_transcript)
print("Summary:", result["summary"])
print("Action Items:", result["action_items"])
print("Decisions:", result["decisions"])
```

## Integration with Zoom RTMS

### Fetching Transcripts from RTMS

```javascript
// JavaScript example
async function getTranscriptFromRTMS(meetingId) {
  const response = await fetch(
    `https://api.zoom.us/v2/meetings/${meetingId}/recordings`,
    {
      headers: {
        Authorization: `Bearer ${process.env.ZOOM_ACCESS_TOKEN}`,
      },
    }
  );
  const data = await response.json();
  // Extract transcript from recording data
  return data.recording_files[0].transcript;
}

// Use with LangChain
async function analyzeMeetingFromZoom(meetingId) {
  const transcript = await getTranscriptFromRTMS(meetingId);
  const analysis = await analyzeMeeting(transcript);
  return analysis;
}
```

```python
# Python example
import requests
import os

def get_transcript_from_rtms(meeting_id):
    headers = {
        "Authorization": f"Bearer {os.getenv('ZOOM_ACCESS_TOKEN')}"
    }
    response = requests.get(
        f"https://api.zoom.us/v2/meetings/{meeting_id}/recordings",
        headers=headers
    )
    data = response.json()
    # Extract transcript from recording data
    return data["recording_files"][0]["transcript"]

# Use with LangChain
def analyze_meeting_from_zoom(meeting_id):
    transcript = get_transcript_from_rtms(meeting_id)
    analysis = analyze_meeting(transcript)
    return analysis
```

## Key Features

- **Modular Chains**: Build reusable chains for different analysis tasks
- **Sequential Processing**: Combine multiple chains for comprehensive analysis
- **Prompt Templates**: Customize prompts for specific meeting analysis needs
- **LLM Flexibility**: Switch between different language models (OpenAI, Anthropic, etc.)
- **Output Parsing**: Structured extraction of insights from unstructured transcripts

## Best Practices

1. **Prompt Engineering**: Craft specific prompts for your use case
2. **Chain Composition**: Use sequential chains for multi-step analysis
3. **Error Handling**: Implement retry logic for API calls
4. **Caching**: Cache transcript analysis to reduce API costs
5. **Validation**: Validate extracted data (action items, decisions) for accuracy

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangChain.js Documentation](https://js.langchain.com/)
- [Zoom API Documentation](https://developers.zoom.us/docs/api/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
