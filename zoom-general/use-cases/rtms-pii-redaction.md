# PII Redaction

## Overview

Replace detected Personally Identifiable Information (PII) with `[REDACTED]` markers in meeting transcripts. This use case demonstrates how to identify and mask sensitive data including email addresses, phone numbers, social security numbers, credit card numbers, and other personal information.

## Use Case

When processing meeting transcripts from Zoom Real-Time Messaging Service (RTMS), you may need to redact sensitive information before storing, sharing, or analyzing the transcript data. This ensures compliance with privacy regulations and protects participant information.

## JavaScript Example

```javascript
// PII Redaction for Zoom Transcripts
class PIIRedactor {
  constructor() {
    // Define PII patterns
    this.patterns = {
      email: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
      phone: /\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b/g,
      ssn: /\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0{4})\d{4}\b/g,
      creditCard: /\b(?:\d{4}[-\s]?){3}\d{4}\b/g,
      ipAddress: /\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b/g,
      passport: /\b[A-Z]{1,2}\d{6,9}\b/g,
      driverLicense: /\b[A-Z]{1,2}\d{5,8}\b/g
    };
  }

  redact(text) {
    let redactedText = text;
    
    // Apply each pattern
    for (const [type, pattern] of Object.entries(this.patterns)) {
      redactedText = redactedText.replace(pattern, '[REDACTED]');
    }
    
    return redactedText;
  }

  redactWithTracking(text) {
    let redactedText = text;
    const findings = {};
    
    // Apply each pattern and track findings
    for (const [type, pattern] of Object.entries(this.patterns)) {
      const matches = text.match(pattern);
      if (matches) {
        findings[type] = matches.length;
        redactedText = redactedText.replace(pattern, `[REDACTED_${type.toUpperCase()}]`);
      }
    }
    
    return {
      redactedText,
      findings,
      totalRedacted: Object.values(findings).reduce((a, b) => a + b, 0)
    };
  }
}

// Usage Example
const redactor = new PIIRedactor();

const transcript = `
Meeting attendees: john.doe@example.com and jane.smith@company.org
John's phone: 555-123-4567
SSN mentioned: 123-45-6789
Credit card: 4532-1234-5678-9010
Server IP: 192.168.1.1
Passport: US123456789
`;

// Simple redaction
const redacted = redactor.redact(transcript);
console.log('Redacted Transcript:');
console.log(redacted);

// Redaction with tracking
const result = redactor.redactWithTracking(transcript);
console.log('\nRedaction Report:');
console.log('Redacted Text:', result.redactedText);
console.log('Findings:', result.findings);
console.log('Total PII Found:', result.totalRedacted);
```

## Python Example

```python
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class RedactionResult:
    redacted_text: str
    findings: Dict[str, int]
    total_redacted: int

class PIIRedactor:
    def __init__(self):
        """Initialize PII patterns for detection and redaction."""
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
            'ssn': r'\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0{4})\d{4}\b',
            'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            'ip_address': r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
            'passport': r'\b[A-Z]{1,2}\d{6,9}\b',
            'driver_license': r'\b[A-Z]{1,2}\d{5,8}\b'
        }
    
    def redact(self, text: str) -> str:
        """
        Redact all detected PII from text.
        
        Args:
            text: Input text containing potential PII
            
        Returns:
            Text with PII replaced by [REDACTED]
        """
        redacted_text = text
        
        for pii_type, pattern in self.patterns.items():
            redacted_text = re.sub(pattern, '[REDACTED]', redacted_text)
        
        return redacted_text
    
    def redact_with_tracking(self, text: str) -> RedactionResult:
        """
        Redact PII and track what was found.
        
        Args:
            text: Input text containing potential PII
            
        Returns:
            RedactionResult with redacted text, findings, and count
        """
        redacted_text = text
        findings = {}
        
        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                findings[pii_type] = len(matches)
                redacted_text = re.sub(
                    pattern, 
                    f'[REDACTED_{pii_type.upper()}]', 
                    redacted_text
                )
        
        total_redacted = sum(findings.values())
        
        return RedactionResult(
            redacted_text=redacted_text,
            findings=findings,
            total_redacted=total_redacted
        )
    
    def redact_selective(self, text: str, pii_types: List[str]) -> str:
        """
        Redact only specific types of PII.
        
        Args:
            text: Input text containing potential PII
            pii_types: List of PII types to redact (e.g., ['email', 'phone'])
            
        Returns:
            Text with selected PII types redacted
        """
        redacted_text = text
        
        for pii_type in pii_types:
            if pii_type in self.patterns:
                pattern = self.patterns[pii_type]
                redacted_text = re.sub(pattern, '[REDACTED]', redacted_text)
        
        return redacted_text

# Usage Example
if __name__ == '__main__':
    redactor = PIIRedactor()
    
    transcript = """
    Meeting attendees: john.doe@example.com and jane.smith@company.org
    John's phone: 555-123-4567
    SSN mentioned: 123-45-6789
    Credit card: 4532-1234-5678-9010
    Server IP: 192.168.1.1
    Passport: US123456789
    """
    
    # Simple redaction
    print("=== Simple Redaction ===")
    redacted = redactor.redact(transcript)
    print(redacted)
    
    # Redaction with tracking
    print("\n=== Redaction with Tracking ===")
    result = redactor.redact_with_tracking(transcript)
    print("Redacted Text:")
    print(result.redacted_text)
    print("\nFindings:")
    for pii_type, count in result.findings.items():
        print(f"  {pii_type}: {count}")
    print(f"\nTotal PII Found: {result.total_redacted}")
    
    # Selective redaction
    print("\n=== Selective Redaction (Email & Phone Only) ===")
    selective = redactor.redact_selective(transcript, ['email', 'phone'])
    print(selective)
```

## Key Features

- **Email Detection**: Identifies standard email address formats
- **Phone Numbers**: Detects various phone number formats (with/without country code)
- **Social Security Numbers**: Identifies SSN patterns with validation
- **Credit Cards**: Detects credit card number patterns
- **IP Addresses**: Identifies IPv4 addresses
- **Passport Numbers**: Detects passport number formats
- **Driver Licenses**: Detects driver license patterns
- **Tracking**: Optional reporting of what PII was found
- **Selective Redaction**: Redact only specific PII types

## Integration with Zoom RTMS

```javascript
// Example: Integrate with Zoom RTMS transcript processing
async function processTranscriptWithRedaction(transcriptData) {
  const redactor = new PIIRedactor();
  
  const processedMessages = transcriptData.messages.map(message => ({
    ...message,
    text: redactor.redact(message.text),
    timestamp: message.timestamp,
    speaker: message.speaker
  }));
  
  return {
    ...transcriptData,
    messages: processedMessages,
    redactionApplied: true
  };
}
```

## Best Practices

1. **Always Redact Before Sharing**: Apply redaction before storing or sharing transcripts
2. **Log Redaction Events**: Track when and what PII was redacted for audit purposes
3. **Test Patterns**: Validate regex patterns against your specific data formats
4. **Consider Context**: Some patterns may have false positives; review and adjust as needed
5. **Compliance**: Ensure redaction meets your organization's privacy and compliance requirements
6. **Backup Original**: Keep original transcripts in secure storage if needed for legal purposes

## Security Considerations

- Store redacted transcripts separately from originals
- Implement access controls on original transcript data
- Log all redaction operations for audit trails
- Consider encryption for sensitive transcript data
- Regularly review and update PII detection patterns
