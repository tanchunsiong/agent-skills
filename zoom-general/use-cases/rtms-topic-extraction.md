# Topic Extraction

Extract main topics from RTMS transcripts using LDA (Latent Dirichlet Allocation) and NMF (Non-negative Matrix Factorization) algorithms.

## Overview

Topic modeling identifies hidden thematic structures in meeting transcripts, enabling automatic categorization and summarization of discussion content.

## JavaScript Implementation

### Using natural (Node.js)

```javascript
const natural = require('natural');
const fs = require('fs');

// Sample RTMS transcript
const transcript = `
The team discussed the Q4 roadmap and feature priorities. 
We reviewed the API performance metrics and identified bottlenecks.
Customer feedback highlighted the need for better documentation.
The infrastructure team presented cloud migration plans.
We scheduled follow-up meetings for each initiative.
`;

// Tokenization and preprocessing
const tokenizer = new natural.WordTokenizer();
const tokens = tokenizer.tokenize(transcript.toLowerCase());

// Remove stopwords
const stopwords = new Set([
  'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
  'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
  'we', 'you', 'i', 'he', 'she', 'it', 'they', 'this', 'that'
]);

const filtered = tokens.filter(token => !stopwords.has(token));

// Term frequency analysis
const termFreq = {};
filtered.forEach(term => {
  termFreq[term] = (termFreq[term] || 0) + 1;
});

// Extract top terms (pseudo-topics)
const topTerms = Object.entries(termFreq)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 10)
  .map(([term, freq]) => ({ term, frequency: freq }));

console.log('Extracted Topics (Top Terms):');
console.log(topTerms);

// Output:
// [
//   { term: 'team', frequency: 2 },
//   { term: 'discussed', frequency: 1 },
//   { term: 'roadmap', frequency: 1 },
//   { term: 'api', frequency: 1 },
//   { term: 'performance', frequency: 1 },
//   ...
// ]
```

### Using gensim-node (Advanced LDA)

```javascript
const { LDA } = require('gensim-node');
const fs = require('fs');

async function extractTopicsLDA() {
  // Sample transcripts
  const transcripts = [
    'The team discussed the Q4 roadmap and feature priorities.',
    'We reviewed the API performance metrics and identified bottlenecks.',
    'Customer feedback highlighted the need for better documentation.',
    'The infrastructure team presented cloud migration plans.',
    'We scheduled follow-up meetings for each initiative.'
  ];

  // Initialize LDA model
  const lda = new LDA({
    numTopics: 3,
    iterations: 100,
    passes: 10,
    alpha: 0.1,
    eta: 0.01
  });

  // Train model
  await lda.train(transcripts);

  // Extract topics
  const topics = await lda.getTopics();
  
  console.log('LDA Topics:');
  topics.forEach((topic, idx) => {
    console.log(`\nTopic ${idx + 1}:`);
    console.log(topic.words.slice(0, 5).join(', '));
  });

  // Get document-topic distribution
  const docTopics = await lda.getDocumentTopics(transcripts[0]);
  console.log('\nDocument-Topic Distribution:');
  console.log(docTopics);
}

extractTopicsLDA().catch(console.error);
```

## Python Implementation

### Using Gensim (LDA)

```python
from gensim import corpora, models
from gensim.parsing.preprocessing import STOPWORDS
import re

# Sample RTMS transcripts
transcripts = [
    "The team discussed the Q4 roadmap and feature priorities.",
    "We reviewed the API performance metrics and identified bottlenecks.",
    "Customer feedback highlighted the need for better documentation.",
    "The infrastructure team presented cloud migration plans.",
    "We scheduled follow-up meetings for each initiative.",
    "Database optimization improved query response times significantly.",
    "Security audit revealed compliance gaps in authentication.",
    "Product team presented user research findings and insights."
]

# Preprocessing
def preprocess(text):
    # Lowercase and remove special characters
    text = re.sub(r'[^a-z\s]', '', text.lower())
    # Tokenize
    tokens = text.split()
    # Remove stopwords
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    return tokens

# Process all transcripts
processed = [preprocess(doc) for doc in transcripts]

# Create dictionary and corpus
dictionary = corpora.Dictionary(processed)
corpus = [dictionary.doc2bow(doc) for doc in processed]

# Train LDA model
lda_model = models.LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=3,
    random_state=42,
    passes=10,
    per_word_topics=True
)

# Display topics
print("LDA Topics:")
for idx, topic in lda_model.print_topics(-1):
    print(f"Topic {idx}: {topic}")

# Get topic distribution for a document
doc_topics = lda_model.get_document_topics(corpus[0])
print(f"\nDocument 0 Topic Distribution:")
for topic_id, prob in doc_topics:
    print(f"  Topic {topic_id}: {prob:.4f}")

# Output:
# LDA Topics:
# Topic 0: '0.009*"team" + 0.008*"discussed" + 0.007*"roadmap"'
# Topic 1: '0.010*"api" + 0.009*"performance" + 0.008*"metrics"'
# Topic 2: '0.011*"customer" + 0.010*"feedback" + 0.009*"documentation"'
```

### Using scikit-learn (NMF)

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import numpy as np

# Sample RTMS transcripts
transcripts = [
    "The team discussed the Q4 roadmap and feature priorities.",
    "We reviewed the API performance metrics and identified bottlenecks.",
    "Customer feedback highlighted the need for better documentation.",
    "The infrastructure team presented cloud migration plans.",
    "We scheduled follow-up meetings for each initiative.",
    "Database optimization improved query response times significantly.",
    "Security audit revealed compliance gaps in authentication.",
    "Product team presented user research findings and insights."
]

# Vectorize documents using TF-IDF
vectorizer = TfidfVectorizer(
    max_features=100,
    stop_words='english',
    min_df=1,
    max_df=0.8
)
tfidf_matrix = vectorizer.fit_transform(transcripts)

# Train NMF model
nmf_model = NMF(
    n_components=3,
    random_state=42,
    init='nndsvd',
    max_iter=500
)
nmf_model.fit(tfidf_matrix)

# Display topics
feature_names = vectorizer.get_feature_names_out()
print("NMF Topics:")
for topic_idx, topic in enumerate(nmf_model.components_):
    top_indices = topic.argsort()[-5:][::-1]
    top_terms = [feature_names[i] for i in top_indices]
    print(f"Topic {topic_idx}: {', '.join(top_terms)}")

# Get topic distribution for a document
doc_topics = nmf_model.transform(tfidf_matrix[0:1])[0]
print(f"\nDocument 0 Topic Distribution:")
for topic_id, prob in enumerate(doc_topics):
    print(f"  Topic {topic_id}: {prob:.4f}")

# Output:
# NMF Topics:
# Topic 0: team, discussed, roadmap, feature, priorities
# Topic 1: api, performance, metrics, bottlenecks, reviewed
# Topic 2: customer, feedback, documentation, need, highlighted
```

## Comparison: LDA vs NMF

| Aspect | LDA | NMF |
|--------|-----|-----|
| **Algorithm** | Probabilistic (Bayesian) | Matrix Factorization |
| **Interpretability** | Probabilistic distributions | Direct term weights |
| **Computational Cost** | Higher (iterative sampling) | Lower (linear algebra) |
| **Best For** | Exploratory analysis | Fast topic extraction |
| **Sparsity** | Dense topics | Sparse topics |

## Integration with RTMS

```python
# Example: Process RTMS API transcript response
import requests
from gensim import corpora, models

def extract_topics_from_rtms(meeting_id, num_topics=5):
    """Extract topics from RTMS meeting transcript"""
    
    # Fetch transcript from RTMS API
    response = requests.get(
        f'https://api.zoom.us/v2/meetings/{meeting_id}/recordings/transcript',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    transcript_data = response.json()
    sentences = [msg['text'] for msg in transcript_data['messages']]
    
    # Preprocess
    processed = [preprocess(sent) for sent in sentences]
    
    # Create corpus
    dictionary = corpora.Dictionary(processed)
    corpus = [dictionary.doc2bow(doc) for doc in processed]
    
    # Train LDA
    lda = models.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        passes=10
    )
    
    return {
        'meeting_id': meeting_id,
        'topics': [
            {
                'id': idx,
                'terms': dict(lda.show_topic(idx, topn=5))
            }
            for idx in range(num_topics)
        ]
    }
```

## Use Cases

- **Meeting Summarization**: Identify key discussion topics automatically
- **Content Categorization**: Route transcripts to relevant teams
- **Trend Analysis**: Track topic evolution across multiple meetings
- **Quality Assurance**: Ensure all agenda items were covered
- **Knowledge Management**: Build searchable topic indexes

## References

- [Gensim Documentation](https://radimrehurek.com/gensim/)
- [scikit-learn NMF](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html)
- [LDA Explained](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)
