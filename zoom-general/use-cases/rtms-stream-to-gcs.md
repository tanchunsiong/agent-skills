# Stream to Google Cloud Storage

Upload Zoom RTMS stream data to Google Cloud Storage.

## JavaScript Example

Using `@google-cloud/storage`:

```javascript
const { Storage } = require('@google-cloud/storage');
const { EventEmitter } = require('events');

// Initialize GCS client
const storage = new Storage({
  projectId: process.env.GCP_PROJECT_ID,
  keyFilename: process.env.GCP_KEY_FILE
});

const bucket = storage.bucket(process.env.GCS_BUCKET_NAME);

// Stream RTMS data to GCS
async function streamToGCS(rtmsStream, fileName) {
  const file = bucket.file(fileName);
  
  const writeStream = file.createWriteStream({
    metadata: {
      contentType: 'application/octet-stream'
    }
  });

  rtmsStream.pipe(writeStream);

  return new Promise((resolve, reject) => {
    writeStream.on('finish', () => {
      console.log(`File ${fileName} uploaded to GCS`);
      resolve();
    });

    writeStream.on('error', (error) => {
      console.error('Upload error:', error);
      reject(error);
    });
  });
}

// Usage
const rtmsStream = getZoomRTMSStream(); // Your RTMS stream source
streamToGCS(rtmsStream, `zoom-stream-${Date.now()}.bin`)
  .catch(console.error);
```

## Python Example

Using `google-cloud-storage`:

```python
from google.cloud import storage
import os

# Initialize GCS client
storage_client = storage.Client(
    project=os.getenv('GCP_PROJECT_ID')
)

bucket = storage_client.bucket(os.getenv('GCS_BUCKET_NAME'))

def stream_to_gcs(rtms_stream, file_name):
    """Upload RTMS stream to Google Cloud Storage."""
    blob = bucket.blob(file_name)
    
    # Upload from stream
    blob.upload_from_file(
        rtms_stream,
        content_type='application/octet-stream',
        rewind=True
    )
    
    print(f"File {file_name} uploaded to GCS")
    return blob.public_url

# Usage
import time
rtms_stream = get_zoom_rtms_stream()  # Your RTMS stream source
file_name = f"zoom-stream-{int(time.time())}.bin"
url = stream_to_gcs(rtms_stream, file_name)
print(f"Uploaded to: {url}")
```

## Setup

### JavaScript
```bash
npm install @google-cloud/storage
```

### Python
```bash
pip install google-cloud-storage
```

## Authentication

Set environment variables:
- `GCP_PROJECT_ID`: Your Google Cloud project ID
- `GCS_BUCKET_NAME`: Target GCS bucket name
- `GCP_KEY_FILE`: Path to service account JSON key (JavaScript)

For Python, use Application Default Credentials or set `GOOGLE_APPLICATION_CREDENTIALS`.
