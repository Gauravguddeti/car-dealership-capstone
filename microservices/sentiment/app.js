const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 5050;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Simple sentiment analysis using keyword matching
function analyzeSentiment(text) {
  if (!text || typeof text !== 'string') {
    return 'neutral';
  }

  const textLower = text.toLowerCase();

  // Define keyword lists
  const positiveWords = [
    'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome', 
    'good', 'best', 'love', 'perfect', 'outstanding', 'brilliant', 
    'superb', 'magnificent', 'marvelous', 'terrific', 'fabulous',
    'recommend', 'happy', 'satisfied', 'pleased', 'impressed',
    'friendly', 'helpful', 'professional', 'courteous', 'efficient'
  ];

  const negativeWords = [
    'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 
    'disappointing', 'poor', 'lousy', 'pathetic', 'useless',
    'annoying', 'frustrating', 'rude', 'unhelpful', 'unprofessional',
    'slow', 'expensive', 'overpriced', 'scam', 'fraud',
    'avoid', 'never', 'regret', 'waste', 'disaster'
  ];

  const neutralWords = [
    'okay', 'average', 'normal', 'fine', 'decent', 'standard',
    'typical', 'regular', 'ordinary', 'moderate', 'fair'
  ];

  // Count matches
  let positiveScore = 0;
  let negativeScore = 0;
  let neutralScore = 0;

  // Check for positive words
  positiveWords.forEach(word => {
    const regex = new RegExp(`\\b${word}\\b`, 'gi');
    const matches = textLower.match(regex);
    if (matches) {
      positiveScore += matches.length;
    }
  });

  // Check for negative words
  negativeWords.forEach(word => {
    const regex = new RegExp(`\\b${word}\\b`, 'gi');
    const matches = textLower.match(regex);
    if (matches) {
      negativeScore += matches.length;
    }
  });

  // Check for neutral words
  neutralWords.forEach(word => {
    const regex = new RegExp(`\\b${word}\\b`, 'gi');
    const matches = textLower.match(regex);
    if (matches) {
      neutralScore += matches.length;
    }
  });

  // Determine sentiment based on scores
  if (positiveScore > negativeScore && positiveScore > neutralScore) {
    return 'positive';
  } else if (negativeScore > positiveScore && negativeScore > neutralScore) {
    return 'negative';
  } else {
    return 'neutral';
  }
}

// Routes

// Analyze sentiment
app.post('/analyze', (req, res) => {
  try {
    const { text } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: 'Text is required' });
    }
    
    const sentiment = analyzeSentiment(text);
    
    res.json({
      text: text,
      sentiment: sentiment,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error analyzing sentiment:', error);
    res.status(500).json({ error: 'Failed to analyze sentiment' });
  }
});

// Batch analyze multiple texts
app.post('/analyze/batch', (req, res) => {
  try {
    const { texts } = req.body;
    
    if (!texts || !Array.isArray(texts)) {
      return res.status(400).json({ error: 'Texts array is required' });
    }
    
    const results = texts.map((text, index) => ({
      index: index,
      text: text,
      sentiment: analyzeSentiment(text)
    }));
    
    res.json({
      results: results,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error analyzing batch sentiment:', error);
    res.status(500).json({ error: 'Failed to analyze batch sentiment' });
  }
});

// Get sentiment statistics for a text
app.post('/analyze/detailed', (req, res) => {
  try {
    const { text } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: 'Text is required' });
    }
    
    const sentiment = analyzeSentiment(text);
    const wordCount = text.split(/\s+/).length;
    const charCount = text.length;
    
    res.json({
      text: text,
      sentiment: sentiment,
      statistics: {
        word_count: wordCount,
        character_count: charCount,
        analyzed_at: new Date().toISOString()
      }
    });
  } catch (error) {
    console.error('Error analyzing detailed sentiment:', error);
    res.status(500).json({ error: 'Failed to analyze detailed sentiment' });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK',
    service: 'Sentiment Analyzer',
    timestamp: new Date().toISOString()
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'Sentiment Analysis API',
    version: '1.0.0',
    endpoints: {
      'POST /analyze': 'Analyze sentiment of a single text',
      'POST /analyze/batch': 'Analyze sentiment of multiple texts',
      'POST /analyze/detailed': 'Get detailed sentiment analysis',
      'GET /health': 'Health check'
    },
    example: {
      endpoint: 'POST /analyze',
      body: {
        text: 'This is a great service!'
      },
      response: {
        text: 'This is a great service!',
        sentiment: 'positive',
        timestamp: '2024-01-01T12:00:00.000Z'
      }
    }
  });
});

app.listen(PORT, () => {
  console.log(`Sentiment Analysis API server running on port ${PORT}`);
  console.log(`Visit http://localhost:${PORT} to see available endpoints`);
});