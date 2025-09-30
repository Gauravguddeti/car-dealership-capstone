# Django Car Dealership Capstone Project

A comprehensive car dealership management system built with Django, featuring user authentication, dealer reviews, and sentiment analysis.

## Features

- User authentication (login, logout, signup)
- Dealer management and reviews
- MongoDB integration with Express.js API
- Sentiment analysis for reviews
- Admin interface for car makes and models
- Responsive web design with Bootstrap
- CI/CD pipeline ready
- Cloud deployment configuration

## Project Structure

```
djangoapp/
├── static/                 # Static files (CSS, JS, images)
├── templates/              # HTML templates
├── models.py              # Django models
├── views.py               # View functions
├── urls.py                # URL routing
├── admin.py               # Admin configuration
├── forms.py               # Django forms
└── apps.py                # App configuration

functions/
├── sample/                # Sentiment analysis microservice
└── requirements.txt       # Python dependencies

server/
├── djangoapp/            # Main Django project
├── database/             # Database scripts
├── Dockerfile            # Docker configuration
└── requirements.txt      # Python dependencies

microservices/
├── dealership/           # Express.js API for dealers
└── sentiment/            # Sentiment analysis service
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Dealer API (Express.js/MongoDB)
- `GET /dealerships` - Get all dealers
- `GET /dealerships/:state` - Get dealers by state
- `GET /reviews/dealer/:id` - Get reviews for a dealer
- `POST /review` - Add a new review

### Sentiment Analysis
- `POST /analyze` - Analyze sentiment of review text

## Deployment

The application is configured for deployment on IBM Cloud with Docker containers.

## Testing

Run tests with:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request