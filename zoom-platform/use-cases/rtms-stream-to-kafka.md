# Stream to Kafka

Publish transcript events from Zoom Real-Time Messaging Service (RTMS) to Apache Kafka for distributed event processing and real-time analytics.

## Overview

This use case demonstrates how to consume transcript events from Zoom RTMS and publish them to a Kafka topic. This enables:

- Real-time transcript processing across multiple consumers
- Event streaming to data pipelines and analytics platforms
- Decoupling of transcript ingestion from downstream processing
- Scalable event distribution to multiple services

## JavaScript Example (kafkajs)

### Installation

```bash
npm install kafkajs
```

### Implementation

```javascript
const { Kafka } = require('kafkajs');
const WebSocket = require('ws');

// Initialize Kafka producer
const kafka = new Kafka({
  clientId: 'zoom-rtms-producer',
  brokers: ['localhost:9092'], // Update with your Kafka brokers
});

const producer = kafka.producer();

// Zoom RTMS WebSocket connection
const ZOOM_RTMS_URL = 'wss://rtms.zoom.us/'; // Update with actual endpoint
const KAFKA_TOPIC = 'zoom-transcripts';

async function connectToZoomRTMS(accessToken) {
  const ws = new WebSocket(ZOOM_RTMS_URL, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  ws.on('open', () => {
    console.log('Connected to Zoom RTMS');
  });

  ws.on('message', async (data) => {
    try {
      const event = JSON.parse(data);

      // Publish to Kafka
      await producer.send({
        topic: KAFKA_TOPIC,
        messages: [
          {
            key: event.meeting_id || 'unknown',
            value: JSON.stringify({
              timestamp: new Date().toISOString(),
              event_type: event.type,
              meeting_id: event.meeting_id,
              user_id: event.user_id,
              transcript_text: event.text,
              language: event.language,
              raw_event: event,
            }),
            headers: {
              'content-type': 'application/json',
              'source': 'zoom-rtms',
            },
          },
        ],
      });

      console.log(`Published event to Kafka: ${event.type}`);
    } catch (error) {
      console.error('Error processing message:', error);
    }
  });

  ws.on('error', (error) => {
    console.error('WebSocket error:', error);
  });

  ws.on('close', () => {
    console.log('Disconnected from Zoom RTMS');
  });

  return ws;
}

async function main() {
  try {
    // Connect Kafka producer
    await producer.connect();
    console.log('Kafka producer connected');

    // Get access token (implement your auth flow)
    const accessToken = process.env.ZOOM_ACCESS_TOKEN;

    // Connect to Zoom RTMS
    await connectToZoomRTMS(accessToken);

    // Keep process alive
    process.on('SIGINT', async () => {
      await producer.disconnect();
      process.exit(0);
    });
  } catch (error) {
    console.error('Fatal error:', error);
    process.exit(1);
  }
}

main();
```

### Configuration

Create a `.env` file:

```env
ZOOM_ACCESS_TOKEN=your_zoom_access_token
KAFKA_BROKERS=localhost:9092
KAFKA_TOPIC=zoom-transcripts
```

### Running

```bash
node rtms-to-kafka.js
```

## Python Example (confluent-kafka)

### Installation

```bash
pip install confluent-kafka websocket-client python-dotenv
```

### Implementation

```python
import json
import logging
import os
import signal
import sys
from datetime import datetime
from typing import Optional

import websocket
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

class ZoomRTMSToKafkaStreamer:
    def __init__(self):
        self.zoom_access_token = os.getenv('ZOOM_ACCESS_TOKEN')
        self.kafka_brokers = os.getenv('KAFKA_BROKERS', 'localhost:9092')
        self.kafka_topic = os.getenv('KAFKA_TOPIC', 'zoom-transcripts')
        
        # Initialize Kafka producer
        self.producer = Producer({
            'bootstrap.servers': self.kafka_brokers,
            'client.id': 'zoom-rtms-producer',
            'acks': 'all',
            'retries': 3,
        })
        
        self.ws = None
        self.running = True

    def delivery_report(self, err, msg):
        """Callback for Kafka delivery reports"""
        if err is not None:
            logger.error(f'Message delivery failed: {err}')
        else:
            logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def on_message(self, ws, message: str):
        """Handle incoming RTMS message"""
        try:
            event = json.loads(message)
            
            # Prepare message for Kafka
            kafka_message = {
                'timestamp': datetime.utcnow().isoformat(),
                'event_type': event.get('type'),
                'meeting_id': event.get('meeting_id'),
                'user_id': event.get('user_id'),
                'transcript_text': event.get('text'),
                'language': event.get('language'),
                'raw_event': event,
            }
            
            # Publish to Kafka
            self.producer.produce(
                topic=self.kafka_topic,
                key=event.get('meeting_id', 'unknown').encode('utf-8'),
                value=json.dumps(kafka_message).encode('utf-8'),
                headers={
                    'content-type': 'application/json',
                    'source': 'zoom-rtms',
                },
                callback=self.delivery_report,
            )
            
            logger.info(f'Published event to Kafka: {event.get("type")}')
            
        except json.JSONDecodeError as e:
            logger.error(f'Failed to parse message: {e}')
        except Exception as e:
            logger.error(f'Error processing message: {e}')

    def on_error(self, ws, error):
        """Handle WebSocket errors"""
        logger.error(f'WebSocket error: {error}')

    def on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket close"""
        logger.info('Disconnected from Zoom RTMS')
        self.running = False

    def on_open(self, ws):
        """Handle WebSocket open"""
        logger.info('Connected to Zoom RTMS')

    def connect_to_zoom_rtms(self):
        """Establish WebSocket connection to Zoom RTMS"""
        zoom_rtms_url = 'wss://rtms.zoom.us/'  # Update with actual endpoint
        
        headers = {
            'Authorization': f'Bearer {self.zoom_access_token}',
        }
        
        self.ws = websocket.WebSocketApp(
            zoom_rtms_url,
            header=headers,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        
        self.ws.run_forever()

    def shutdown(self, signum, frame):
        """Handle graceful shutdown"""
        logger.info('Shutting down...')
        self.running = False
        if self.ws:
            self.ws.close()
        self.producer.flush()
        sys.exit(0)

    def run(self):
        """Start the streamer"""
        # Register signal handlers
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        
        try:
            logger.info('Starting Zoom RTMS to Kafka streamer')
            self.connect_to_zoom_rtms()
        except Exception as e:
            logger.error(f'Fatal error: {e}')
            sys.exit(1)


if __name__ == '__main__':
    streamer = ZoomRTMSToKafkaStreamer()
    streamer.run()
```

### Configuration

Create a `.env` file:

```env
ZOOM_ACCESS_TOKEN=your_zoom_access_token
KAFKA_BROKERS=localhost:9092
KAFKA_TOPIC=zoom-transcripts
```

### Running

```bash
python rtms_to_kafka.py
```

## Kafka Topic Schema

Recommended topic configuration:

```bash
kafka-topics.sh --create \
  --topic zoom-transcripts \
  --partitions 3 \
  --replication-factor 2 \
  --config retention.ms=604800000 \
  --config compression.type=snappy
```

## Message Format

Messages published to Kafka follow this structure:

```json
{
  "timestamp": "2024-01-27T10:30:45.123Z",
  "event_type": "transcript.text",
  "meeting_id": "meeting_123",
  "user_id": "user_456",
  "transcript_text": "Hello, this is a test transcript",
  "language": "en-US",
  "raw_event": {
    "type": "transcript.text",
    "meeting_id": "meeting_123",
    "user_id": "user_456",
    "text": "Hello, this is a test transcript",
    "language": "en-US"
  }
}
```

## Best Practices

1. **Partitioning**: Use `meeting_id` as the Kafka message key to ensure all events from a meeting go to the same partition
2. **Error Handling**: Implement retry logic and dead-letter queues for failed messages
3. **Monitoring**: Track producer metrics (latency, throughput, errors)
4. **Authentication**: Use OAuth 2.0 for Zoom API authentication
5. **Compression**: Enable Snappy or LZ4 compression for better throughput
6. **Retention**: Set appropriate retention policies based on your use case

## Downstream Processing

Example Kafka consumer for processing transcripts:

```javascript
// JavaScript consumer example
const consumer = kafka.consumer({ groupId: 'transcript-processors' });
await consumer.subscribe({ topic: 'zoom-transcripts' });

await consumer.run({
  eachMessage: async ({ topic, partition, message }) => {
    const event = JSON.parse(message.value.toString());
    // Process transcript event
    console.log(`Processing: ${event.transcript_text}`);
  },
});
```

## Troubleshooting

- **Connection Issues**: Verify Zoom RTMS endpoint and access token validity
- **Kafka Errors**: Check broker connectivity and topic configuration
- **Message Loss**: Enable producer acknowledgments and configure retries
- **Performance**: Monitor partition distribution and consumer lag

## Related Resources

- [Zoom RTMS Documentation](https://developers.zoom.us/)
- [KafkaJS Documentation](https://kafka.js.org/)
- [Confluent Kafka Python](https://docs.confluent.io/kafka-clients/python/current/overview.html)
- [Kafka Best Practices](https://kafka.apache.org/documentation/#bestpractices)
