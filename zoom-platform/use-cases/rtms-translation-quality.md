# Translation Quality Assessment

Evaluate and improve translation quality for RTMS transcripts.

## Overview

Monitor and improve translation accuracy with quality metrics and feedback loops.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
class TranslationQualityAssessor {
  constructor(options = {}) {
    this.referenceTranslator = options.referenceTranslator;
    this.metrics = [];
  }
  
  async assessQuality(original, translation, targetLang) {
    const scores = {};
    
    // Length ratio check
    scores.lengthRatio = this.checkLengthRatio(original, translation);
    
    // Placeholder preservation
    scores.placeholderPreservation = this.checkPlaceholders(original, translation);
    
    // Number preservation
    scores.numberPreservation = this.checkNumbers(original, translation);
    
    // If reference translator available, compare
    if (this.referenceTranslator) {
      const reference = await this.referenceTranslator.translate(original, targetLang);
      scores.similarity = this.calculateSimilarity(translation, reference);
    }
    
    // Overall score
    const weights = {
      lengthRatio: 0.2,
      placeholderPreservation: 0.3,
      numberPreservation: 0.3,
      similarity: 0.2
    };
    
    let overallScore = 0;
    let totalWeight = 0;
    
    for (const [metric, weight] of Object.entries(weights)) {
      if (scores[metric] !== undefined) {
        overallScore += scores[metric] * weight;
        totalWeight += weight;
      }
    }
    
    scores.overall = totalWeight > 0 ? overallScore / totalWeight : 0;
    
    this.metrics.push({
      timestamp: Date.now(),
      original,
      translation,
      targetLang,
      scores
    });
    
    return scores;
  }
  
  checkLengthRatio(original, translation) {
    const expectedRatios = {
      // Target language expansion factors
      de: 1.3,  // German tends to be longer
      fr: 1.2,
      es: 1.25,
      ja: 0.8,  // Japanese tends to be shorter
      zh: 0.6
    };
    
    const ratio = translation.length / original.length;
    const expected = expectedRatios.de || 1; // Default
    
    // Score based on how close to expected ratio
    const deviation = Math.abs(ratio - expected) / expected;
    return Math.max(0, 1 - deviation);
  }
  
  checkPlaceholders(original, translation) {
    const placeholderRegex = /\{[^}]+\}|\[[^\]]+\]|%\w+/g;
    const originalPlaceholders = original.match(placeholderRegex) || [];
    const translationPlaceholders = translation.match(placeholderRegex) || [];
    
    if (originalPlaceholders.length === 0) return 1;
    
    const preserved = originalPlaceholders.filter(p => 
      translationPlaceholders.includes(p)
    ).length;
    
    return preserved / originalPlaceholders.length;
  }
  
  checkNumbers(original, translation) {
    const numberRegex = /\d+(?:[.,]\d+)?%?/g;
    const originalNumbers = original.match(numberRegex) || [];
    const translationNumbers = translation.match(numberRegex) || [];
    
    if (originalNumbers.length === 0) return 1;
    
    const preserved = originalNumbers.filter(n => 
      translationNumbers.some(tn => 
        tn.replace(/[.,]/g, '') === n.replace(/[.,]/g, '')
      )
    ).length;
    
    return preserved / originalNumbers.length;
  }
  
  calculateSimilarity(text1, text2) {
    // Simple word overlap similarity
    const words1 = new Set(text1.toLowerCase().split(/\s+/));
    const words2 = new Set(text2.toLowerCase().split(/\s+/));
    
    const intersection = [...words1].filter(w => words2.has(w)).length;
    const union = new Set([...words1, ...words2]).size;
    
    return intersection / union; // Jaccard similarity
  }
  
  getAverageScores() {
    if (this.metrics.length === 0) return null;
    
    const totals = { overall: 0, lengthRatio: 0, placeholderPreservation: 0, numberPreservation: 0 };
    const counts = { ...totals };
    
    for (const m of this.metrics) {
      for (const key of Object.keys(totals)) {
        if (m.scores[key] !== undefined) {
          totals[key] += m.scores[key];
          counts[key]++;
        }
      }
    }
    
    const averages = {};
    for (const key of Object.keys(totals)) {
      averages[key] = counts[key] > 0 ? totals[key] / counts[key] : 0;
    }
    
    return averages;
  }
  
  getLowQualityTranslations(threshold = 0.7) {
    return this.metrics.filter(m => m.scores.overall < threshold);
  }
  
  generateReport() {
    const averages = this.getAverageScores();
    const lowQuality = this.getLowQualityTranslations();
    
    return {
      totalTranslations: this.metrics.length,
      averageScores: averages,
      lowQualityCount: lowQuality.length,
      lowQualityPercentage: (lowQuality.length / this.metrics.length) * 100,
      recommendations: this.generateRecommendations(averages)
    };
  }
  
  generateRecommendations(averages) {
    const recommendations = [];
    
    if (averages.numberPreservation < 0.9) {
      recommendations.push('Consider using a glossary for number formatting');
    }
    if (averages.lengthRatio < 0.7) {
      recommendations.push('Translation length seems off - check for truncation');
    }
    if (averages.placeholderPreservation < 0.9) {
      recommendations.push('Placeholders are being lost - use placeholder protection');
    }
    
    return recommendations;
  }
}

// Usage
const assessor = new TranslationQualityAssessor();

receiver.onTranscript = async (segment) => {
  const translation = await translator.translate(segment.text, 'es');
  
  const quality = await assessor.assessQuality(segment.text, translation, 'es');
  
  if (quality.overall < 0.7) {
    console.warn('Low quality translation detected:', segment.text);
  }
  
  displayCaption(translation);
};

// Generate report at end
const report = assessor.generateReport();
console.log('Translation Quality Report:', report);
```

## Resources

- **BLEU score**: https://en.wikipedia.org/wiki/BLEU
- **RTMS docs**: https://developers.zoom.us/docs/rtms/
