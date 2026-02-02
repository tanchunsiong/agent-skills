# RAG-Powered Customer Support

Build a RAG-powered customer support assistant that uses RTMS transcripts to search a knowledge base and provide real-time answers.

## Overview

This use case creates an AI customer support assistant that combines Zoom RTMS transcripts with Retrieval-Augmented Generation (RAG). When customers ask questions during a Zoom meeting, the system retrieves relevant context from your knowledge base documents (PDF, TXT, DOCX, MD) using semantic search, then generates accurate, grounded answers via an LLM. Results are displayed in a web frontend via WebSocket.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
import { RTMSManager } from './library/javascript/rtmsManager/RTMSManager.js';
import WebhookManager from './library/javascript/webhookManager/WebhookManager.js';
import { FrontendManager } from './library/javascript/rtmsManager/FrontendManager.js';
import { FrontendWssManager } from './library/javascript/rtmsManager/FrontendWssManager.js';
import { preloadRetrieverOnce, askLLMWithTranscript } from './ragPipeline.js';
import express from 'express';
import http from 'http';

// Preload document retriever at startup
await preloadRetrieverOnce();

const { MEDIA_PARAMS } = RTMSManager;

const rtmsConfig = {
  logging: 'info',
  credentials: {
    meeting: {
      clientId: process.env.ZOOM_CLIENT_ID,
      clientSecret: process.env.ZOOM_CLIENT_SECRET,
      zoomSecretToken: process.env.ZOOM_SECRET_TOKEN,
    },
  },
  mediaParams: {
    audio: {
      contentType: MEDIA_PARAMS.MEDIA_CONTENT_TYPE_RTP,
      sampleRate: MEDIA_PARAMS.AUDIO_SAMPLE_RATE_SR_16K,
      channel: MEDIA_PARAMS.AUDIO_CHANNEL_MONO,
      codec: MEDIA_PARAMS.MEDIA_PAYLOAD_TYPE_L16,
      dataOpt: MEDIA_PARAMS.MEDIA_DATA_OPTION_AUDIO_MIXED_STREAM,
      sendRate: 100,
    },
    transcript: {
      contentType: MEDIA_PARAMS.MEDIA_CONTENT_TYPE_TEXT,
      language: MEDIA_PARAMS.LANGUAGE_ID_ENGLISH,
    },
  }
};

const app = express();
const server = http.createServer(app);

await RTMSManager.init(rtmsConfig);

// Set up frontend UI and WebSocket for real-time display
const frontendManager = new FrontendManager({
  config: {
    port: 3000,
    serveStaticEnabled: true,
    viewsPath: './views',
    frontendWssUrl: process.env.FRONTEND_WSS_URL_TO_CONNECT_TO || '',
    frontendWssPath: '/ws'
  },
  app: app
});
frontendManager.setup();

const frontendWssManager = new FrontendWssManager({
  config: { frontendWssEnabled: true, frontendWssPath: '/ws' },
  server: server
});
frontendWssManager.setup();

const webhookManager = new WebhookManager({
  config: {
    webhookPath: process.env.WEBHOOK_PATH || '/',
    zoomSecretToken: rtmsConfig.credentials.meeting.zoomSecretToken,
  },
  app: app
});

webhookManager.on('event', (event, payload) => {
  RTMSManager.handleEvent(event, payload);
});
webhookManager.setup();

// Process transcripts through RAG pipeline
RTMSManager.on('transcript', async ({ text, userName }) => {
  console.log('Transcript received:', text);
  const result = await askLLMWithTranscript(text);
  frontendWssManager.broadcastToFrontendClients({
    type: 'transcript',
    content: result,
    user: userName,
    timestamp: Date.now()
  });
});

RTMSManager.on('meeting.rtms_started', (payload) => {
  console.log(`RTMS started for meeting ${payload.meeting_uuid}`);
});

await RTMSManager.start();

server.listen(3000, () => {
  console.log('Server running at http://localhost:3000');
});
```

#### RAG Pipeline Module

```javascript
// ragPipeline.js - Document loading, embedding, and contextual QA
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { MemoryVectorStore } from 'langchain/vectorstores/memory';

let retriever = null;

export async function preloadRetrieverOnce() {
  // Load documents from docs/ folder (PDF, TXT, DOCX, MD)
  const docs = await loadDocuments('./docs');
  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: 1000,
    chunkOverlap: 150,
  });
  const chunks = await splitter.splitDocuments(docs);
  const vectorStore = await MemoryVectorStore.fromDocuments(chunks, embeddings);
  retriever = vectorStore.asRetriever();
}

export async function askLLMWithTranscript(transcript) {
  const relevantDocs = await retriever.getRelevantDocuments(transcript);
  const context = relevantDocs.map(d => d.pageContent).join('\n');

  const prompt = `
  <scenario>
    <role>customer_support</role>
    <input>
      <transcript>${transcript}</transcript>
      <context>${context}</context>
    </input>
    <instruction>
      Use the context to answer the customer's question from the transcript.
      Be helpful, concise, and format in bullet points.
      Only respond using information from the transcript or context.
    </instruction>
  </scenario>`;

  // Send to LLM via OpenRouter and return response
  return await queryLLM(prompt);
}
```

### Python

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

class RAGCustomerSupport:
    def __init__(self, docs_path='./docs'):
        self.embeddings = HuggingFaceEmbeddings(model_name='thenlper/gte-small')
        self.retriever = None
        self._load_docs(docs_path)

    def _load_docs(self, docs_path):
        # Load and split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=150
        )
        # Load from PDF, TXT, DOCX, MD files
        chunks = splitter.split_documents(self._read_docs(docs_path))
        store = FAISS.from_documents(chunks, self.embeddings)
        self.retriever = store.as_retriever()

    def answer(self, transcript: str) -> str:
        docs = self.retriever.get_relevant_documents(transcript)
        context = '\n'.join(d.page_content for d in docs)
        prompt = f"Context: {context}\nQuestion: {transcript}\nAnswer helpfully:"
        return query_llm(prompt)
```

## Resources

- **Sample repo**: https://github.com/zoom/rtms-samples/tree/main/zoom_apps/ai_rag_customer_support_js
- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **LangChain**: https://js.langchain.com/docs/
- **OpenRouter**: https://openrouter.ai/docs
