# Stream to AWS S3

Upload audio/video/transcripts to AWS S3.

## Overview

This guide demonstrates how to stream Zoom Real-Time Messaging Service (RTMS) data including audio, video, and transcripts directly to AWS S3 for persistent storage and archival.

## Prerequisites

- AWS account with S3 bucket created
- AWS credentials configured (Access Key ID and Secret Access Key)
- Zoom RTMS connection established
- Node.js 14+ (for JavaScript) or Python 3.7+ (for Python)

## JavaScript Example (AWS SDK)

### Installation

```bash
npm install aws-sdk
```

### Code

```javascript
const AWS = require('aws-sdk');
const fs = require('fs');
const path = require('path');

// Configure AWS credentials
AWS.config.update({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION || 'us-east-1'
});

const s3 = new AWS.S3();

/**
 * Upload stream data to S3
 * @param {string} bucketName - S3 bucket name
 * @param {string} key - S3 object key (path)
 * @param {Buffer|Stream} data - Data to upload
 * @param {string} contentType - MIME type
 */
async function uploadToS3(bucketName, key, data, contentType = 'application/octet-stream') {
  try {
    const params = {
      Bucket: bucketName,
      Key: key,
      Body: data,
      ContentType: contentType,
      ServerSideEncryption: 'AES256'
    };

    const result = await s3.upload(params).promise();
    console.log(`Successfully uploaded to s3://${bucketName}/${key}`);
    return result;
  } catch (error) {
    console.error('Error uploading to S3:', error);
    throw error;
  }
}

/**
 * Upload audio stream from RTMS
 */
async function uploadAudioStream(bucketName, meetingId, audioBuffer) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const key = `zoom-recordings/${meetingId}/audio/${timestamp}.wav`;
  
  return uploadToS3(bucketName, key, audioBuffer, 'audio/wav');
}

/**
 * Upload video stream from RTMS
 */
async function uploadVideoStream(bucketName, meetingId, videoBuffer) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const key = `zoom-recordings/${meetingId}/video/${timestamp}.mp4`;
  
  return uploadToS3(bucketName, key, videoBuffer, 'video/mp4');
}

/**
 * Upload transcript to S3
 */
async function uploadTranscript(bucketName, meetingId, transcriptData) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const key = `zoom-recordings/${meetingId}/transcripts/${timestamp}.json`;
  
  const transcriptJson = JSON.stringify(transcriptData, null, 2);
  return uploadToS3(bucketName, key, Buffer.from(transcriptJson), 'application/json');
}

// Example usage
(async () => {
  const bucketName = process.env.S3_BUCKET_NAME || 'my-zoom-recordings';
  const meetingId = 'meeting-123456';
  
  try {
    // Upload audio
    const audioBuffer = Buffer.from('audio data here');
    await uploadAudioStream(bucketName, meetingId, audioBuffer);
    
    // Upload video
    const videoBuffer = Buffer.from('video data here');
    await uploadVideoStream(bucketName, meetingId, videoBuffer);
    
    // Upload transcript
    const transcript = {
      meetingId,
      timestamp: new Date().toISOString(),
      content: [
        { speaker: 'John', text: 'Hello everyone' },
        { speaker: 'Jane', text: 'Hi John' }
      ]
    };
    await uploadTranscript(bucketName, meetingId, transcript);
  } catch (error) {
    console.error('Upload failed:', error);
    process.exit(1);
  }
})();
```

## Python Example (Boto3)

### Installation

```bash
pip install boto3
```

### Code

```python
import boto3
import json
from datetime import datetime
from typing import Union, Dict, Any
import os

class ZoomS3Uploader:
    """Upload Zoom RTMS streams to AWS S3"""
    
    def __init__(self, bucket_name: str, region: str = 'us-east-1'):
        """
        Initialize S3 uploader
        
        Args:
            bucket_name: S3 bucket name
            region: AWS region
        """
        self.s3_client = boto3.client(
            's3',
            region_name=region,
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        self.bucket_name = bucket_name
    
    def upload_to_s3(
        self,
        key: str,
        data: Union[bytes, str],
        content_type: str = 'application/octet-stream'
    ) -> Dict[str, Any]:
        """
        Upload data to S3
        
        Args:
            key: S3 object key (path)
            data: Data to upload (bytes or string)
            content_type: MIME type
            
        Returns:
            S3 response metadata
        """
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            response = self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=data,
                ContentType=content_type,
                ServerSideEncryption='AES256'
            )
            
            print(f"Successfully uploaded to s3://{self.bucket_name}/{key}")
            return response
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            raise
    
    def upload_audio_stream(self, meeting_id: str, audio_data: bytes) -> Dict[str, Any]:
        """Upload audio stream from RTMS"""
        timestamp = datetime.now().isoformat().replace(':', '-')
        key = f"zoom-recordings/{meeting_id}/audio/{timestamp}.wav"
        return self.upload_to_s3(key, audio_data, 'audio/wav')
    
    def upload_video_stream(self, meeting_id: str, video_data: bytes) -> Dict[str, Any]:
        """Upload video stream from RTMS"""
        timestamp = datetime.now().isoformat().replace(':', '-')
        key = f"zoom-recordings/{meeting_id}/video/{timestamp}.mp4"
        return self.upload_to_s3(key, video_data, 'video/mp4')
    
    def upload_transcript(self, meeting_id: str, transcript_data: Dict[str, Any]) -> Dict[str, Any]:
        """Upload transcript to S3"""
        timestamp = datetime.now().isoformat().replace(':', '-')
        key = f"zoom-recordings/{meeting_id}/transcripts/{timestamp}.json"
        
        transcript_json = json.dumps(transcript_data, indent=2)
        return self.upload_to_s3(key, transcript_json, 'application/json')


# Example usage
if __name__ == '__main__':
    bucket_name = os.getenv('S3_BUCKET_NAME', 'my-zoom-recordings')
    meeting_id = 'meeting-123456'
    
    uploader = ZoomS3Uploader(bucket_name)
    
    try:
        # Upload audio
        audio_data = b'audio data here'
        uploader.upload_audio_stream(meeting_id, audio_data)
        
        # Upload video
        video_data = b'video data here'
        uploader.upload_video_stream(meeting_id, video_data)
        
        # Upload transcript
        transcript = {
            'meetingId': meeting_id,
            'timestamp': datetime.now().isoformat(),
            'content': [
                {'speaker': 'John', 'text': 'Hello everyone'},
                {'speaker': 'Jane', 'text': 'Hi John'}
            ]
        }
        uploader.upload_transcript(meeting_id, transcript)
        
    except Exception as e:
        print(f"Upload failed: {e}")
        exit(1)
```

## Configuration

### Environment Variables

```bash
# AWS credentials
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1

# S3 bucket
export S3_BUCKET_NAME=my-zoom-recordings
```

### S3 Bucket Policy

Ensure your S3 bucket has appropriate permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::YOUR_ACCOUNT_ID:user/YOUR_USER"
      },
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-zoom-recordings",
        "arn:aws:s3:::my-zoom-recordings/*"
      ]
    }
  ]
}
```

## Best Practices

1. **Encryption**: Always enable server-side encryption (AES256 or KMS)
2. **Versioning**: Enable S3 versioning for audit trails
3. **Lifecycle Policies**: Set up lifecycle rules to transition old recordings to Glacier
4. **Access Control**: Use IAM roles with least privilege
5. **Monitoring**: Enable CloudTrail and S3 access logging
6. **Error Handling**: Implement retry logic with exponential backoff
7. **Naming Convention**: Use consistent naming for easy retrieval (meetingId/type/timestamp)

## Troubleshooting

- **Access Denied**: Verify AWS credentials and S3 bucket permissions
- **Network Timeout**: Check AWS region configuration and network connectivity
- **Large Files**: Use multipart upload for files > 100MB
- **Rate Limiting**: Implement backoff strategy for high-volume uploads

## References

- [AWS SDK for JavaScript](https://docs.aws.amazon.com/sdk-for-javascript/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [S3 Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/BestPractices.html)
