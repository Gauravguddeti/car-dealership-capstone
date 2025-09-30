import json
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm, ReviewForm
from .models import CarMake, CarModel, Dealer, DealerReview


# API endpoints for microservices
DEALERSHIP_API_URL = "http://localhost:3030"
SENTIMENT_API_URL = "http://localhost:5050"


def get_dealerships(request, state=None):
    """Get all dealerships or filter by state"""
    try:
        if state:
            url = f"{DEALERSHIP_API_URL}/dealerships/{state}"
        else:
            url = f"{DEALERSHIP_API_URL}/dealerships"
        
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except:
        # Return dummy data if API is not available
        return [
            {
                "id": 1,
                "city": "Brooklyn",
                "state": "New York", 
                "st": "NY",
                "address": "123 Main St",
                "zip": "11201",
                "lat": 40.6892,
                "long": -73.9442,
                "short_name": "Brooklyn Motors",
                "full_name": "Brooklyn Motors Car Dealership"
            },
            {
                "id": 2,
                "city": "Austin",
                "state": "Texas",
                "st": "TX", 
                "address": "456 Oak Ave",
                "zip": "73301",
                "lat": 30.2672,
                "long": -97.7431,
                "short_name": "Austin Auto",
                "full_name": "Austin Auto Sales"
            },
            {
                "id": 3,
                "city": "Topeka",
                "state": "Kansas",
                "st": "KS",
                "address": "789 Pine St",
                "zip": "66603",
                "lat": 39.0473,
                "long": -95.6890,
                "short_name": "Kansas Cars",
                "full_name": "Kansas Car Center"
            }
        ]


def get_dealer_reviews(dealer_id):
    """Get reviews for a specific dealer"""
    try:
        url = f"{DEALERSHIP_API_URL}/reviews/dealer/{dealer_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except:
        # Return actual database reviews if API is not available
        from .models import DealerReview
        reviews = DealerReview.objects.filter(dealership=dealer_id)
        review_list = []
        for review in reviews:
            review_list.append({
                "id": review.id,
                "name": review.name,
                "dealership": review.dealership,
                "review": review.review,
                "purchase": review.purchase,
                "purchase_date": review.purchase_date.strftime('%Y-%m-%d') if review.purchase_date else '',
                "car_make": review.car_make,
                "car_model": review.car_model,
                "car_year": review.car_year,
                "sentiment": review.sentiment
            })
        return review_list


def analyze_sentiment(text):
    """Analyze sentiment of review text"""
    try:
        url = f"{SENTIMENT_API_URL}/analyze"
        payload = {"text": text}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result.get("sentiment", "neutral")
        else:
            return "neutral"
    except:
        # Simple sentiment analysis fallback
        positive_words = ['great', 'excellent', 'good', 'amazing', 'wonderful', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'disappointing']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"


def index(request):
    """Main homepage view"""
    state = request.GET.get('state', '')
    dealerships = get_dealerships(request, state if state else None)
    
    context = {
        'dealerships': dealerships,
        'states': ['New York', 'Texas', 'Kansas', 'California', 'Florida'],
        'selected_state': state
    }
    return render(request, 'djangoapp/index.html', context)


def about(request):
    """About page view"""
    return render(request, 'djangoapp/about.html')


def contact(request):
    """Contact page view"""
    return render(request, 'djangoapp/contact.html')


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('djangoapp:index')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'djangoapp/login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('djangoapp:index')


def signup_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('djangoapp:login')
    else:
        form = SignUpForm()
    
    return render(request, 'djangoapp/signup.html', {'form': form})


def dealer_details(request, dealer_id):
    """Dealer details page with reviews"""
    dealerships = get_dealerships(request)
    dealer = next((d for d in dealerships if d['id'] == int(dealer_id)), None)
    
    if not dealer:
        messages.error(request, 'Dealer not found.')
        return redirect('djangoapp:index')
    
    reviews = get_dealer_reviews(dealer_id)
    
    context = {
        'dealer': dealer,
        'reviews': reviews
    }
    return render(request, 'djangoapp/dealer_details.html', context)


@login_required
def add_review(request, dealer_id):
    """Add review for a dealer"""
    dealerships = get_dealerships(request)
    dealer = next((d for d in dealerships if d['id'] == int(dealer_id)), None)
    
    if not dealer:
        messages.error(request, 'Dealer not found.')
        return redirect('djangoapp:index')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.dealership = int(dealer_id)
            
            # Analyze sentiment
            sentiment = analyze_sentiment(review.review)
            review.sentiment = sentiment
            
            review.save()
            
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'dealer': dealer,
        'car_makes': CarMake.objects.all(),
        'car_models': CarModel.objects.all()
    }
    return render(request, 'djangoapp/add_review.html', context)


@csrf_exempt
def get_cars(request):
    """API endpoint to get car makes and models"""
    if request.method == 'GET':
        car_makes = list(CarMake.objects.values())
        return JsonResponse({'car_makes': car_makes})
    
    return JsonResponse({'error': 'Invalid request method'})


# API Views for testing
def dealerships_api(request):
    """API view to show all dealerships"""
    dealerships = get_dealerships(request)
    return JsonResponse({'dealerships': dealerships})


def dealerships_by_state_api(request, state):
    """API view to show dealerships by state"""
    dealerships = get_dealerships(request, state)
    return JsonResponse({'dealerships': dealerships})


def dealer_reviews_api(request, dealer_id):
    """API view to show dealer reviews"""
    reviews = get_dealer_reviews(dealer_id)
    return JsonResponse({'reviews': reviews})


def sentiment_analyzer_api(request):
    """API view to test sentiment analyzer"""
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')
        sentiment = analyze_sentiment(text)
        return JsonResponse({
            'text': text,
            'sentiment': sentiment
        })
    
    # For GET requests, show a simple form
    return render(request, 'djangoapp/sentiment_test.html')