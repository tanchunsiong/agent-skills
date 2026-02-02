# PII Detection

Detect personally identifiable information using regex patterns and Named Entity Recognition (NER) techniques.

## Overview

Personally Identifiable Information (PII) includes sensitive data such as:
- Social Security Numbers (SSN)
- Credit card numbers
- Email addresses
- Phone numbers
- Names and addresses

This guide demonstrates how to detect these patterns using both regex-based approaches and NLP-based Named Entity Recognition.

## JavaScript Examples

### Regex-Based Detection

```javascript
// SSN Detection (XXX-XX-XXXX format)
const ssnRegex = /\b\d{3}-\d{2}-\d{4}\b/g;
const detectSSN = (text) => {
  return text.match(ssnRegex) || [];
};

// Credit Card Detection (Visa, Mastercard, Amex)
const creditCardRegex = /\b(?:\d{4}[-\s]?){3}\d{4}\b/g;
const detectCreditCard = (text) => {
  return text.match(creditCardRegex) || [];
};

// Email Detection
const emailRegex = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g;
const detectEmail = (text) => {
  return text.match(emailRegex) || [];
};

// Phone Number Detection (US format)
const phoneRegex = /\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b/g;
const detectPhone = (text) => {
  return text.match(phoneRegex) || [];
};

// Comprehensive PII Detection
const detectPII = (text) => {
  return {
    ssns: detectSSN(text),
    creditCards: detectCreditCard(text),
    emails: detectEmail(text),
    phones: detectPhone(text)
  };
};

// Usage Example
const sampleText = `
  Contact John at john.doe@example.com or 555-123-4567.
  SSN: 123-45-6789
  Card: 4532-1234-5678-9010
`;

console.log(detectPII(sampleText));
```

### NER-Based Detection with Node.js

```javascript
// Using compromise NLP library for entity recognition
const nlp = require('compromise');

const detectPIIWithNER = (text) => {
  const doc = nlp(text);
  
  // Extract named entities
  const people = doc.people().out('array');
  const organizations = doc.organizations().out('array');
  
  // Combine with regex patterns
  const regexPII = detectPII(text);
  
  return {
    entities: {
      people,
      organizations
    },
    patterns: regexPII
  };
};

// Usage
const result = detectPIIWithNER(sampleText);
console.log(result);
```

## Python Examples

### Regex-Based Detection

```python
import re

class PIIDetector:
    """Detect PII using regex patterns"""
    
    # SSN pattern: XXX-XX-XXXX
    SSN_PATTERN = r'\b\d{3}-\d{2}-\d{4}\b'
    
    # Credit card pattern: 4532-1234-5678-9010
    CREDIT_CARD_PATTERN = r'\b(?:\d{4}[-\s]?){3}\d{4}\b'
    
    # Email pattern
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # US Phone pattern: (555) 123-4567 or 555-123-4567
    PHONE_PATTERN = r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
    
    @staticmethod
    def detect_ssn(text):
        """Detect Social Security Numbers"""
        return re.findall(PIIDetector.SSN_PATTERN, text)
    
    @staticmethod
    def detect_credit_cards(text):
        """Detect credit card numbers"""
        return re.findall(PIIDetector.CREDIT_CARD_PATTERN, text)
    
    @staticmethod
    def detect_emails(text):
        """Detect email addresses"""
        return re.findall(PIIDetector.EMAIL_PATTERN, text)
    
    @staticmethod
    def detect_phones(text):
        """Detect phone numbers"""
        return re.findall(PIIDetector.PHONE_PATTERN, text)
    
    @staticmethod
    def detect_all(text):
        """Detect all PII types"""
        return {
            'ssns': PIIDetector.detect_ssn(text),
            'credit_cards': PIIDetector.detect_credit_cards(text),
            'emails': PIIDetector.detect_emails(text),
            'phones': PIIDetector.detect_phones(text)
        }

# Usage Example
sample_text = """
Contact John at john.doe@example.com or 555-123-4567.
SSN: 123-45-6789
Card: 4532-1234-5678-9010
"""

detector = PIIDetector()
results = detector.detect_all(sample_text)
print(results)
```

### NER-Based Detection with spaCy

```python
import spacy
import re

class PIIDetectorNER:
    """Detect PII using spaCy NER and regex patterns"""
    
    def __init__(self):
        # Load English language model
        self.nlp = spacy.load('en_core_web_sm')
        self.regex_detector = PIIDetector()
    
    def detect_with_ner(self, text):
        """Detect PII using Named Entity Recognition"""
        doc = self.nlp(text)
        
        # Extract entities
        entities = {
            'PERSON': [],
            'ORG': [],
            'GPE': [],
            'EMAIL': [],
            'PHONE': [],
            'SSN': [],
            'CREDIT_CARD': []
        }
        
        # NER-based detection
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        # Regex-based detection
        entities['EMAIL'] = self.regex_detector.detect_emails(text)
        entities['PHONE'] = self.regex_detector.detect_phones(text)
        entities['SSN'] = self.regex_detector.detect_ssn(text)
        entities['CREDIT_CARD'] = self.regex_detector.detect_credit_cards(text)
        
        return entities
    
    def redact_pii(self, text, replacement='[REDACTED]'):
        """Redact detected PII from text"""
        redacted = text
        
        # Redact SSNs
        redacted = re.sub(PIIDetector.SSN_PATTERN, replacement, redacted)
        
        # Redact credit cards
        redacted = re.sub(PIIDetector.CREDIT_CARD_PATTERN, replacement, redacted)
        
        # Redact emails
        redacted = re.sub(PIIDetector.EMAIL_PATTERN, replacement, redacted)
        
        # Redact phone numbers
        redacted = re.sub(PIIDetector.PHONE_PATTERN, replacement, redacted)
        
        return redacted

# Usage Example
detector_ner = PIIDetectorNER()
sample_text = """
Contact John at john.doe@example.com or 555-123-4567.
SSN: 123-45-6789
Card: 4532-1234-5678-9010
"""

# Detect PII
pii_results = detector_ner.detect_with_ner(sample_text)
print("Detected PII:", pii_results)

# Redact PII
redacted_text = detector_ner.redact_pii(sample_text)
print("Redacted Text:", redacted_text)
```

## Best Practices

1. **Combine Approaches**: Use both regex and NER for comprehensive detection
2. **Validate Results**: Regex patterns may produce false positives; validate with additional checks
3. **Redaction**: Always redact or mask detected PII before logging or storing
4. **Privacy Compliance**: Ensure PII detection aligns with GDPR, CCPA, and other regulations
5. **Performance**: For large documents, consider streaming or chunking text
6. **Regular Updates**: Keep regex patterns and NER models updated

## Integration with Zoom Platform

When integrating PII detection with Zoom's Real-Time Messaging Service:

1. Process messages in real-time before storage
2. Flag messages containing PII for review
3. Implement automatic redaction policies
4. Log PII detection events for compliance audits
5. Provide user notifications when PII is detected

## References

- [OWASP PII Detection](https://owasp.org/www-community/attacks/PII_Detection)
- [spaCy Named Entity Recognition](https://spacy.io/usage/linguistic-features#named-entities)
- [Regular Expression Patterns](https://www.regular-expressions.info/)
