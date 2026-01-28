# Video Face Detection

Detect and track faces in RTMS video streams.

## Overview

Detect faces for attendance tracking, emotion analysis, or engagement monitoring.

## Skills Needed

- **zoom-rtms** - Primary

## Detection Methods

| Method | Speed | Accuracy |
|--------|-------|----------|
| OpenCV Haar | Fast | Good |
| OpenCV DNN | Medium | Very Good |
| MediaPipe | Fast | Excellent |
| face_recognition | Slow | Excellent |

## Implementation

### JavaScript - face-api.js

```javascript
const faceapi = require('@vladmandic/face-api');
const canvas = require('canvas');

// Setup canvas for Node.js
const { Canvas, Image, ImageData } = canvas;
faceapi.env.monkeyPatch({ Canvas, Image, ImageData });

class FaceDetector {
  constructor() {
    this.initialized = false;
    this.onFaceDetected = null;
    this.faceDescriptors = new Map(); // For face recognition
  }
  
  async init() {
    await faceapi.nets.ssdMobilenetv1.loadFromDisk('./models');
    await faceapi.nets.faceLandmark68Net.loadFromDisk('./models');
    await faceapi.nets.faceRecognitionNet.loadFromDisk('./models');
    await faceapi.nets.faceExpressionNet.loadFromDisk('./models');
    
    this.initialized = true;
    console.log('Face detection models loaded');
  }
  
  async detectFaces(frameBuffer, width, height) {
    if (!this.initialized) {
      throw new Error('Not initialized');
    }
    
    // Create canvas from buffer
    const img = new Image();
    img.width = width;
    img.height = height;
    
    const cvs = new Canvas(width, height);
    const ctx = cvs.getContext('2d');
    
    // Draw RGB buffer to canvas
    const imageData = new ImageData(
      new Uint8ClampedArray(frameBuffer),
      width,
      height
    );
    ctx.putImageData(imageData, 0, 0);
    
    // Detect faces with landmarks and expressions
    const detections = await faceapi
      .detectAllFaces(cvs)
      .withFaceLandmarks()
      .withFaceExpressions()
      .withFaceDescriptors();
    
    const results = detections.map((d, i) => ({
      index: i,
      box: {
        x: d.detection.box.x,
        y: d.detection.box.y,
        width: d.detection.box.width,
        height: d.detection.box.height
      },
      confidence: d.detection.score,
      landmarks: d.landmarks.positions,
      expressions: d.expressions,
      descriptor: d.descriptor
    }));
    
    if (results.length > 0) {
      this.onFaceDetected?.(results);
    }
    
    return results;
  }
  
  async recognizeFace(descriptor) {
    // Compare with known faces
    let bestMatch = null;
    let bestDistance = 0.6; // Threshold
    
    for (const [name, knownDescriptor] of this.faceDescriptors) {
      const distance = faceapi.euclideanDistance(descriptor, knownDescriptor);
      if (distance < bestDistance) {
        bestDistance = distance;
        bestMatch = name;
      }
    }
    
    return bestMatch;
  }
  
  registerFace(name, descriptor) {
    this.faceDescriptors.set(name, descriptor);
  }
}

// Usage
const detector = new FaceDetector();
await detector.init();

detector.onFaceDetected = async (faces) => {
  for (const face of faces) {
    console.log(`Face detected: confidence ${face.confidence.toFixed(2)}`);
    console.log(`Expression: ${getDominantExpression(face.expressions)}`);
    
    // Try to recognize
    const name = await detector.recognizeFace(face.descriptor);
    if (name) {
      console.log(`Recognized: ${name}`);
    }
  }
};

ws.on('message', async (data) => {
   try {
     const message = JSON.parse(data.toString());
     
     // Handle keep-alive
     if (message.msg_type === 13) {
       console.log('Keep-alive received');
       return;
     }
     
     // Handle video frame (msg_type 15)
     if (message.msg_type === 15) {
       // Decode base64 video data
       const videoBuffer = Buffer.from(message.data, 'base64');
       const frame = await decodeFrame(videoBuffer);
       await detector.detectFaces(frame.data, frame.width, frame.height);
     }
   } catch (error) {
     console.error('Message parsing error:', error);
   }
});

function getDominantExpression(expressions) {
  return Object.entries(expressions)
    .reduce((a, b) => a[1] > b[1] ? a : b)[0];
}
```

### Python - MediaPipe

```python
import mediapipe as mp
import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FaceDetection:
    index: int
    box: dict
    confidence: float
    landmarks: Optional[List] = None

class FaceDetector:
    def __init__(self, min_confidence=0.5):
        self.mp_face = mp.solutions.face_detection
        self.mp_mesh = mp.solutions.face_mesh
        
        self.detector = self.mp_face.FaceDetection(
            min_detection_confidence=min_confidence
        )
        self.mesh = self.mp_mesh.FaceMesh(
            max_num_faces=10,
            min_detection_confidence=min_confidence
        )
        
        self.on_face_detected = None
    
    def detect(self, frame: np.ndarray) -> List[FaceDetection]:
        # Convert to RGB
        if len(frame.shape) == 3 and frame.shape[2] == 3:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            rgb = frame
        
        results = self.detector.process(rgb)
        
        detections = []
        if results.detections:
            for i, detection in enumerate(results.detections):
                bbox = detection.location_data.relative_bounding_box
                h, w = frame.shape[:2]
                
                face = FaceDetection(
                    index=i,
                    box={
                        'x': int(bbox.xmin * w),
                        'y': int(bbox.ymin * h),
                        'width': int(bbox.width * w),
                        'height': int(bbox.height * h)
                    },
                    confidence=detection.score[0]
                )
                detections.append(face)
        
        if detections and self.on_face_detected:
            self.on_face_detected(detections)
        
        return detections
    
    def detect_with_landmarks(self, frame: np.ndarray):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mesh.process(rgb)
        
        faces = []
        if results.multi_face_landmarks:
            h, w = frame.shape[:2]
            
            for i, landmarks in enumerate(results.multi_face_landmarks):
                points = []
                for lm in landmarks.landmark:
                    points.append({
                        'x': int(lm.x * w),
                        'y': int(lm.y * h),
                        'z': lm.z
                    })
                
                # Calculate bounding box from landmarks
                xs = [p['x'] for p in points]
                ys = [p['y'] for p in points]
                
                faces.append({
                    'index': i,
                    'landmarks': points,
                    'box': {
                        'x': min(xs),
                        'y': min(ys),
                        'width': max(xs) - min(xs),
                        'height': max(ys) - min(ys)
                    }
                })
        
        return faces
    
    def close(self):
        self.detector.close()
        self.mesh.close()

# Face Recognition with face_recognition library
import face_recognition

class FaceRecognizer:
    def __init__(self):
        self.known_faces = {}  # name -> encoding
    
    def register_face(self, name: str, image: np.ndarray):
        encodings = face_recognition.face_encodings(image)
        if encodings:
            self.known_faces[name] = encodings[0]
            return True
        return False
    
    def recognize(self, frame: np.ndarray):
        # Find faces and encodings
        locations = face_recognition.face_locations(frame)
        encodings = face_recognition.face_encodings(frame, locations)
        
        results = []
        for location, encoding in zip(locations, encodings):
            # Compare with known faces
            matches = face_recognition.compare_faces(
                list(self.known_faces.values()),
                encoding,
                tolerance=0.6
            )
            
            name = "Unknown"
            if True in matches:
                idx = matches.index(True)
                name = list(self.known_faces.keys())[idx]
            
            top, right, bottom, left = location
            results.append({
                'name': name,
                'box': {
                    'x': left,
                    'y': top,
                    'width': right - left,
                    'height': bottom - top
                }
            })
        
        return results

# Usage
detector = FaceDetector(min_confidence=0.7)
recognizer = FaceRecognizer()

def on_faces(faces):
    for face in faces:
        print(f"Face {face.index}: {face.confidence:.2f} at {face.box}")

detector.on_face_detected = on_faces

async for raw_message in ws:
     try:
         message = json.loads(raw_message)
         
         # Handle keep-alive
         if message.get('msg_type') == 13:
             print('Keep-alive received')
             continue
         
         # Handle video frame (msg_type 15)
         if message.get('msg_type') == 15:
             # Decode base64 video data
             import base64
             video_buffer = base64.b64decode(message.get('data', ''))
             frame = decode_frame(video_buffer)
             faces = detector.detect(frame)
             
             if faces:
                 recognized = recognizer.recognize(frame)
                 for r in recognized:
                     print(f"{r['name']} detected")
     except json.JSONDecodeError as e:
         print(f'Message parsing error: {e}')
```

## Use Cases

| Use Case | Method |
|----------|--------|
| Attendance | Face recognition |
| Engagement | Expression analysis |
| Count participants | Detection only |
| Emotion tracking | Landmark + expression |

## Resources

- **face-api.js**: https://github.com/vladmandic/face-api
- **MediaPipe**: https://mediapipe.dev/
- **face_recognition**: https://github.com/ageitgey/face_recognition
- **RTMS docs**: https://developers.zoom.us/docs/rtms/
