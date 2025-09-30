const express = require('express');
const { MongoClient } = require('mongodb');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3030;

// MongoDB connection
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017';
const DB_NAME = 'dealership_db';

let db;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Connect to MongoDB
MongoClient.connect(MONGODB_URI)
  .then(client => {
    console.log('Connected to MongoDB');
    db = client.db(DB_NAME);
    
    // Initialize sample data if collections are empty
    initializeSampleData();
  })
  .catch(error => {
    console.error('MongoDB connection error:', error);
    // Continue without MongoDB for development
    console.log('Running without MongoDB - using sample data');
  });

// Sample data for development
const sampleDealerships = [
  {
    id: 1,
    city: "Brooklyn",
    state: "New York",
    st: "NY",
    address: "123 Main St",
    zip: "11201",
    lat: 40.6892,
    long: -73.9442,
    short_name: "Brooklyn Motors",
    full_name: "Brooklyn Motors Car Dealership"
  },
  {
    id: 2,
    city: "Austin",
    state: "Texas",
    st: "TX",
    address: "456 Oak Ave",
    zip: "73301",
    lat: 30.2672,
    long: -97.7431,
    short_name: "Austin Auto",
    full_name: "Austin Auto Sales"
  },
  {
    id: 3,
    city: "Topeka",
    state: "Kansas",
    st: "KS", 
    address: "789 Pine St",
    zip: "66603",
    lat: 39.0473,
    long: -95.6890,
    short_name: "Kansas Cars",
    full_name: "Kansas Car Center"
  },
  {
    id: 4,
    city: "Los Angeles",
    state: "California",
    st: "CA",
    address: "321 Sunset Blvd",
    zip: "90028",
    lat: 34.0522,
    long: -118.2437,
    short_name: "LA Motors",
    full_name: "Los Angeles Premium Motors"
  },
  {
    id: 5,
    city: "Miami",
    state: "Florida",
    st: "FL",
    address: "654 Ocean Dr",
    zip: "33139",
    lat: 25.7617,
    long: -80.1918,
    short_name: "Miami Auto",
    full_name: "Miami Beach Auto Gallery"
  }
];

const sampleReviews = [
  {
    id: 1,
    name: "John Doe",
    dealership: 1,
    review: "Great service and friendly staff. Highly recommend!",
    purchase: true,
    purchase_date: "2023-10-15",
    car_make: "Toyota",
    car_model: "Camry",
    car_year: 2023,
    sentiment: "positive"
  },
  {
    id: 2,
    name: "Jane Smith", 
    dealership: 1,
    review: "Average experience. Could be better.",
    purchase: false,
    purchase_date: "2023-09-20",
    car_make: "Honda",
    car_model: "Civic",
    car_year: 2022,
    sentiment: "neutral"
  },
  {
    id: 3,
    name: "Mike Johnson",
    dealership: 2,
    review: "Excellent customer service! Found exactly what I was looking for.",
    purchase: true,
    purchase_date: "2023-11-01",
    car_make: "Ford",
    car_model: "F-150",
    car_year: 2023,
    sentiment: "positive"
  },
  {
    id: 4,
    name: "Sarah Wilson",
    dealership: 3,
    review: "Professional staff and great selection of vehicles.",
    purchase: true,
    purchase_date: "2023-10-28",
    car_make: "Chevrolet",
    car_model: "Silverado",
    car_year: 2023,
    sentiment: "positive"
  }
];

async function initializeSampleData() {
  if (!db) return;
  
  try {
    // Check if collections exist and have data
    const dealershipsCount = await db.collection('dealerships').countDocuments();
    const reviewsCount = await db.collection('reviews').countDocuments();
    
    if (dealershipsCount === 0) {
      await db.collection('dealerships').insertMany(sampleDealerships);
      console.log('Sample dealerships inserted');
    }
    
    if (reviewsCount === 0) {
      await db.collection('reviews').insertMany(sampleReviews);
      console.log('Sample reviews inserted');
    }
  } catch (error) {
    console.error('Error initializing sample data:', error);
  }
}

// Routes

// Get all dealerships
app.get('/dealerships', async (req, res) => {
  try {
    if (db) {
      const dealerships = await db.collection('dealerships').find({}).toArray();
      res.json(dealerships);
    } else {
      res.json(sampleDealerships);
    }
  } catch (error) {
    console.error('Error fetching dealerships:', error);
    res.json(sampleDealerships);
  }
});

// Get dealerships by state
app.get('/dealerships/:state', async (req, res) => {
  const state = req.params.state;
  
  try {
    if (db) {
      const dealerships = await db.collection('dealerships').find({ 
        state: new RegExp(state, 'i') 
      }).toArray();
      res.json(dealerships);
    } else {
      const filtered = sampleDealerships.filter(d => 
        d.state.toLowerCase().includes(state.toLowerCase())
      );
      res.json(filtered);
    }
  } catch (error) {
    console.error('Error fetching dealerships by state:', error);
    const filtered = sampleDealerships.filter(d => 
      d.state.toLowerCase().includes(state.toLowerCase())
    );
    res.json(filtered);
  }
});

// Get reviews for a specific dealer
app.get('/reviews/dealer/:id', async (req, res) => {
  const dealerId = parseInt(req.params.id);
  
  try {
    if (db) {
      const reviews = await db.collection('reviews').find({ 
        dealership: dealerId 
      }).toArray();
      res.json(reviews);
    } else {
      const filtered = sampleReviews.filter(r => r.dealership === dealerId);
      res.json(filtered);
    }
  } catch (error) {
    console.error('Error fetching reviews:', error);
    const filtered = sampleReviews.filter(r => r.dealership === dealerId);
    res.json(filtered);
  }
});

// Add a new review
app.post('/review', async (req, res) => {
  try {
    const reviewData = {
      ...req.body,
      id: Date.now(), // Simple ID generation
      dealership: parseInt(req.body.dealership)
    };
    
    if (db) {
      const result = await db.collection('reviews').insertOne(reviewData);
      res.json({ success: true, id: result.insertedId });
    } else {
      sampleReviews.push(reviewData);
      res.json({ success: true, id: reviewData.id });
    }
  } catch (error) {
    console.error('Error adding review:', error);
    res.status(500).json({ error: 'Failed to add review' });
  }
});

// Get dealer details by ID
app.get('/dealer/:id', async (req, res) => {
  const dealerId = parseInt(req.params.id);
  
  try {
    if (db) {
      const dealer = await db.collection('dealerships').findOne({ id: dealerId });
      if (dealer) {
        res.json(dealer);
      } else {
        res.status(404).json({ error: 'Dealer not found' });
      }
    } else {
      const dealer = sampleDealerships.find(d => d.id === dealerId);
      if (dealer) {
        res.json(dealer);
      } else {
        res.status(404).json({ error: 'Dealer not found' });
      }
    }
  } catch (error) {
    console.error('Error fetching dealer details:', error);
    res.status(500).json({ error: 'Failed to fetch dealer details' });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    database: db ? 'Connected' : 'Not Connected'
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'Car Dealership API',
    version: '1.0.0',
    endpoints: {
      'GET /dealerships': 'Get all dealerships',
      'GET /dealerships/:state': 'Get dealerships by state',
      'GET /reviews/dealer/:id': 'Get reviews for a dealer',
      'POST /review': 'Add a new review',
      'GET /dealer/:id': 'Get dealer details',
      'GET /health': 'Health check'
    }
  });
});

app.listen(PORT, () => {
  console.log(`Dealership API server running on port ${PORT}`);
  console.log(`Visit http://localhost:${PORT} to see available endpoints`);
});