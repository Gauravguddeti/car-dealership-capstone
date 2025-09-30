from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    # Dealer and reviews
    path('dealer/<int:dealer_id>/', views.dealer_details, name='dealer_details'),
    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),
    
    # API endpoints for testing
    path('api/dealerships/', views.dealerships_api, name='dealerships_api'),
    path('api/dealerships/<str:state>/', views.dealerships_by_state_api, name='dealerships_by_state_api'),
    path('api/reviews/dealer/<int:dealer_id>/', views.dealer_reviews_api, name='dealer_reviews_api'),
    path('api/cars/', views.get_cars, name='get_cars'),
    path('api/sentiment/', views.sentiment_analyzer_api, name='sentiment_analyzer_api'),
]