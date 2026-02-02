# HuggingFace Integration

## Overview

Integrate RTMS (Real-Time Messaging Service) with HuggingFace transformers for advanced NLP tasks. This integration enables real-time text processing, sentiment analysis, named entity recognition, and other transformer-based NLP operations on Zoom meeting transcripts and chat messages.

## Use Cases

- **Real-time Sentiment Analysis**: Analyze participant sentiment during meetings
- **Named Entity Recognition**: Extract entities from meeting discussions
- **Text Classification**: Categorize meeting topics and discussions
- **Question Answering**: Extract answers from meeting content
- **Summarization**: Generate meeting summaries in real-time

## JavaScript Integration

### Setup

```javascript
import { HfInference } from "@huggingface/inference";

const hf = new HfInference(process.env.HUGGINGFACE_API_KEY);

// Connect to RTMS
const rtmsClient = new RTMSClient({
  accessToken: process.env.ZOOM_ACCESS_TOKEN,
});
```

### Sentiment Analysis Example

```javascript
async function analyzeSentimentRTMS(message) {
  try {
    const result = await hf.textClassification({
      model: "distilbert-base-uncased-finetuned-sst-2-english",
      inputs: message,
    });

    return {
      text: message,
      sentiment: result[0].label,
      score: result[0].score,
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    console.error("Sentiment analysis error:", error);
    throw error;
  }
}

// Listen to RTMS messages
rtmsClient.on("message", async (event) => {
  const analysis = await analyzeSentimentRTMS(event.body);
  console.log("Sentiment Analysis:", analysis);

  // Store or process results
  await storeAnalysis(analysis);
});
```

### Named Entity Recognition Example

```javascript
async function extractEntitiesRTMS(text) {
  try {
    const result = await hf.tokenClassification({
      model: "dslim/bert-base-uncased-ner",
      inputs: text,
    });

    // Group entities by type
    const entities = {};
    result.forEach((entity) => {
      if (!entities[entity.entity_group]) {
        entities[entity.entity_group] = [];
      }
      entities[entity.entity_group].push({
        word: entity.word,
        score: entity.score,
      });
    });

    return entities;
  } catch (error) {
    console.error("NER error:", error);
    throw error;
  }
}

// Process meeting transcript
rtmsClient.on("transcript_update", async (event) => {
  const entities = await extractEntitiesRTMS(event.transcript);
  console.log("Extracted Entities:", entities);
});
```

### Question Answering Example

```javascript
async function answerQuestionRTMS(context, question) {
  try {
    const result = await hf.questionAnswering({
      model: "deepset/roberta-base-squad2",
      inputs: {
        question: question,
        context: context,
      },
    });

    return {
      answer: result.answer,
      score: result.score,
      start: result.start,
      end: result.end,
    };
  } catch (error) {
    console.error("QA error:", error);
    throw error;
  }
}

// Handle Q&A during meetings
rtmsClient.on("question", async (event) => {
  const answer = await answerQuestionRTMS(
    event.meetingContext,
    event.question
  );
  console.log("Answer:", answer);
});
```

### Streaming Text Generation Example

```javascript
async function generateSummaryRTMS(transcript) {
  try {
    const stream = await hf.textGenerationStream({
      model: "gpt2",
      inputs: `Summarize this meeting transcript:\n${transcript}`,
      parameters: {
        max_new_tokens: 100,
        temperature: 0.7,
      },
    });

    let summary = "";
    for await (const chunk of stream) {
      summary += chunk.token.text;
      console.log("Streaming:", chunk.token.text);
    }

    return summary;
  } catch (error) {
    console.error("Generation error:", error);
    throw error;
  }
}
```

## Python Integration

### Setup

```python
from transformers import pipeline
from huggingface_hub import InferenceClient
import asyncio

# Initialize HuggingFace client
hf_client = InferenceClient(api_key="YOUR_HUGGINGFACE_API_KEY")

# Initialize pipelines for different tasks
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

ner_pipeline = pipeline(
    "token-classification",
    model="dslim/bert-base-uncased-ner",
    aggregation_strategy="simple"
)

qa_pipeline = pipeline(
    "question-answering",
    model="deepset/roberta-base-squad2"
)
```

### Sentiment Analysis Example

```python
def analyze_sentiment(text):
    """Analyze sentiment of text using transformers"""
    try:
        result = sentiment_pipeline(text)
        return {
            "text": text,
            "label": result[0]["label"],
            "score": result[0]["score"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        raise

# Process RTMS messages
async def process_rtms_messages(rtms_stream):
    async for message in rtms_stream:
        analysis = analyze_sentiment(message["body"])
        print(f"Sentiment: {analysis}")
        await store_analysis(analysis)
```

### Named Entity Recognition Example

```python
def extract_entities(text):
    """Extract named entities from text"""
    try:
        entities = ner_pipeline(text)
        
        # Group by entity type
        grouped = {}
        for entity in entities:
            entity_type = entity["entity_group"]
            if entity_type not in grouped:
                grouped[entity_type] = []
            grouped[entity_type].append({
                "word": entity["word"],
                "score": entity["score"]
            })
        
        return grouped
    except Exception as e:
        print(f"NER error: {e}")
        raise

# Extract entities from meeting transcript
transcript = "John Smith from Microsoft discussed the Q4 results in New York."
entities = extract_entities(transcript)
print(f"Entities: {entities}")
# Output: {
#   "PER": [{"word": "John Smith", "score": 0.99}],
#   "ORG": [{"word": "Microsoft", "score": 0.98}],
#   "LOC": [{"word": "New York", "score": 0.97}]
# }
```

### Question Answering Example

```python
def answer_question(context, question):
    """Answer questions based on context"""
    try:
        result = qa_pipeline(
            question=question,
            context=context
        )
        return {
            "answer": result["answer"],
            "score": result["score"],
            "start": result["start"],
            "end": result["end"]
        }
    except Exception as e:
        print(f"QA error: {e}")
        raise

# Example usage
context = "The meeting was held on January 15, 2024. Attendees discussed Q1 targets."
question = "When was the meeting held?"
answer = answer_question(context, question)
print(f"Answer: {answer['answer']}")  # Output: "January 15, 2024"
```

### Text Summarization Example

```python
from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def summarize_transcript(transcript):
    """Generate summary of meeting transcript"""
    try:
        # Split long transcripts into chunks
        max_length = 1024
        chunks = [
            transcript[i:i+max_length]
            for i in range(0, len(transcript), max_length)
        ]
        
        summaries = []
        for chunk in chunks:
            result = summarizer(chunk, max_length=150, min_length=50)
            summaries.append(result[0]["summary_text"])
        
        return " ".join(summaries)
    except Exception as e:
        print(f"Summarization error: {e}")
        raise

# Process meeting transcript
transcript = """
The quarterly meeting was held on January 15, 2024.
John Smith presented the Q4 financial results showing 15% growth.
Sarah Johnson discussed the new product roadmap for Q1.
The team agreed on three main initiatives for the upcoming quarter.
"""

summary = summarize_transcript(transcript)
print(f"Summary: {summary}")
```

### Batch Processing Example

```python
async def batch_process_messages(messages):
    """Process multiple messages efficiently"""
    results = {
        "sentiments": [],
        "entities": [],
        "classifications": []
    }
    
    for message in messages:
        # Sentiment analysis
        sentiment = analyze_sentiment(message["text"])
        results["sentiments"].append(sentiment)
        
        # Entity extraction
        entities = extract_entities(message["text"])
        results["entities"].append(entities)
    
    return results

# Example batch processing
messages = [
    {"text": "Great meeting today!", "id": 1},
    {"text": "John from Microsoft discussed the project.", "id": 2},
    {"text": "The deadline is March 15, 2024.", "id": 3}
]

results = await batch_process_messages(messages)
```

## Inference API Integration

### JavaScript with Inference API

```javascript
async function useInferenceAPI(task, inputs) {
  const response = await fetch(
    `https://api-inference.huggingface.co/models/${task.model}`,
    {
      headers: { Authorization: `Bearer ${process.env.HUGGINGFACE_API_KEY}` },
      method: "POST",
      body: JSON.stringify(inputs),
    }
  );

  return response.json();
}

// Sentiment analysis via API
const sentiment = await useInferenceAPI(
  { model: "distilbert-base-uncased-finetuned-sst-2-english" },
  { inputs: "This meeting was productive!" }
);
```

### Python with Inference API

```python
import requests

def use_inference_api(model_id, inputs):
    """Call HuggingFace Inference API"""
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}
    
    response = requests.post(api_url, headers=headers, json=inputs)
    return response.json()

# Example: Sentiment analysis
result = use_inference_api(
    "distilbert-base-uncased-finetuned-sst-2-english",
    {"inputs": "Excellent presentation!"}
)
print(result)
```

## Best Practices

1. **Rate Limiting**: Implement rate limiting to avoid API throttling
2. **Caching**: Cache model results for identical inputs
3. **Error Handling**: Implement robust error handling and retries
4. **Batch Processing**: Process multiple messages in batches for efficiency
5. **Model Selection**: Choose appropriate models based on latency/accuracy tradeoffs
6. **Monitoring**: Track API usage and model performance metrics
7. **Security**: Store API keys securely using environment variables

## Performance Considerations

- **Local Models**: Use local transformers for lower latency
- **Quantization**: Use quantized models for faster inference
- **GPU Acceleration**: Enable GPU for faster processing
- **Async Processing**: Use async/await for non-blocking operations
- **Model Caching**: Cache loaded models to avoid reload overhead

## Resources

- [HuggingFace Transformers Documentation](https://huggingface.co/docs/transformers)
- [HuggingFace Inference API](https://huggingface.co/docs/api-inference)
- [HuggingFace Model Hub](https://huggingface.co/models)
- [RTMS Documentation](https://developers.zoom.us/docs/rtms)
