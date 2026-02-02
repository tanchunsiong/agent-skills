# Email Meeting Summary

Send meeting summaries via email using nodemailer (JavaScript) and smtplib (Python).

## Overview

This use case demonstrates how to automatically send meeting summaries to participants via email after a Zoom meeting concludes. The examples use nodemailer for Node.js and smtplib for Python.

## JavaScript Example (nodemailer)

```javascript
const nodemailer = require('nodemailer');
const axios = require('axios');

// Configure your email transporter
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASSWORD
  }
});

// Function to fetch meeting details from Zoom API
async function getMeetingDetails(meetingId, accessToken) {
  try {
    const response = await axios.get(
      `https://api.zoom.us/v2/meetings/${meetingId}`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      }
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching meeting details:', error);
    throw error;
  }
}

// Function to send email summary
async function sendMeetingSummary(meetingId, accessToken, recipientEmail) {
  try {
    // Get meeting details
    const meeting = await getMeetingDetails(meetingId, accessToken);

    // Create email content
    const emailContent = `
      <h2>Meeting Summary: ${meeting.topic}</h2>
      <p><strong>Date:</strong> ${meeting.start_time}</p>
      <p><strong>Duration:</strong> ${meeting.duration} minutes</p>
      <p><strong>Meeting ID:</strong> ${meeting.id}</p>
      <p><strong>Participants:</strong> ${meeting.participants_count || 'N/A'}</p>
      <hr>
      <p>Thank you for attending the meeting. Please review the details above.</p>
    `;

    // Send email
    const mailOptions = {
      from: process.env.EMAIL_USER,
      to: recipientEmail,
      subject: `Meeting Summary: ${meeting.topic}`,
      html: emailContent
    };

    const info = await transporter.sendMail(mailOptions);
    console.log('Email sent:', info.response);
    return info;
  } catch (error) {
    console.error('Error sending email:', error);
    throw error;
  }
}

// Example usage
async function main() {
  const meetingId = '123456789';
  const accessToken = 'YOUR_ZOOM_ACCESS_TOKEN';
  const recipientEmail = 'participant@example.com';

  await sendMeetingSummary(meetingId, accessToken, recipientEmail);
}

main().catch(console.error);
```

## Python Example (smtplib)

```python
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Function to fetch meeting details from Zoom API
def get_meeting_details(meeting_id, access_token):
    """Fetch meeting details from Zoom API"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    try:
        response = requests.get(
            f'https://api.zoom.us/v2/meetings/{meeting_id}',
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching meeting details: {e}')
        raise

# Function to send email summary
def send_meeting_summary(meeting_id, access_token, recipient_email):
    """Send meeting summary via email"""
    
    try:
        # Get meeting details
        meeting = get_meeting_details(meeting_id, access_token)
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Meeting Summary: {meeting['topic']}"
        msg['From'] = os.getenv('EMAIL_USER')
        msg['To'] = recipient_email
        
        # Create HTML content
        html_content = f"""
        <html>
            <body>
                <h2>Meeting Summary: {meeting['topic']}</h2>
                <p><strong>Date:</strong> {meeting['start_time']}</p>
                <p><strong>Duration:</strong> {meeting['duration']} minutes</p>
                <p><strong>Meeting ID:</strong> {meeting['id']}</p>
                <p><strong>Participants:</strong> {meeting.get('participants_count', 'N/A')}</p>
                <hr>
                <p>Thank you for attending the meeting. Please review the details above.</p>
            </body>
        </html>
        """
        
        # Attach HTML content
        part = MIMEText(html_content, 'html')
        msg.attach(part)
        
        # Send email via SMTP
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        email_user = os.getenv('EMAIL_USER')
        email_password = os.getenv('EMAIL_PASSWORD')
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(msg)
        
        print(f'Email sent successfully to {recipient_email}')
        return True
        
    except Exception as e:
        print(f'Error sending email: {e}')
        raise

# Example usage
if __name__ == '__main__':
    meeting_id = '123456789'
    access_token = 'YOUR_ZOOM_ACCESS_TOKEN'
    recipient_email = 'participant@example.com'
    
    send_meeting_summary(meeting_id, access_token, recipient_email)
```

## Environment Variables

Both examples require the following environment variables:

```bash
# Email Configuration
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Zoom API
ZOOM_ACCESS_TOKEN=your-zoom-access-token
```

## Setup Instructions

### JavaScript (Node.js)

1. Install dependencies:
```bash
npm install nodemailer axios
```

2. Set environment variables in `.env` file
3. Run the script:
```bash
node send-summary.js
```

### Python

1. Install dependencies:
```bash
pip install requests
```

2. Set environment variables
3. Run the script:
```bash
python send_summary.py
```

## Key Features

- **Automatic Summaries**: Fetch meeting details from Zoom API
- **HTML Emails**: Format summaries with HTML for better presentation
- **Error Handling**: Comprehensive error handling for API and email failures
- **Flexible Configuration**: Environment-based configuration for credentials
- **Multi-recipient**: Can be extended to send to multiple participants

## Notes

- For Gmail, use [App Passwords](https://support.google.com/accounts/answer/185833) instead of your regular password
- Ensure your Zoom API credentials have appropriate scopes for meeting data access
- Consider implementing retry logic for production environments
- Store sensitive credentials securely using environment variables or secret management services
