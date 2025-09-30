from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import CarMake, CarModel


class DjangoAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test data
        self.car_make = CarMake.objects.create(
            name='Toyota',
            description='Japanese automotive manufacturer'
        )
        
        self.car_model = CarModel.objects.create(
            car_make=self.car_make,
            name='Camry',
            type='SEDAN',
            year=2023
        )

    def test_index_view(self):
        """Test the main index page"""
        response = self.client.get(reverse('djangoapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Car Dealerships')

    def test_about_view(self):
        """Test the about page"""
        response = self.client.get(reverse('djangoapp:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About Us')

    def test_contact_view(self):
        """Test the contact page"""
        response = self.client.get(reverse('djangoapp:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Us')

    def test_login_view(self):
        """Test the login page"""
        response = self.client.get(reverse('djangoapp:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_signup_view(self):
        """Test the signup page"""
        response = self.client.get(reverse('djangoapp:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up')

    def test_user_login(self):
        """Test user authentication"""
        response = self.client.post(reverse('djangoapp:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_dealer_details_view(self):
        """Test dealer details page"""
        response = self.client.get(reverse('djangoapp:dealer_details', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_add_review_requires_login(self):
        """Test that add review requires authentication"""
        response = self.client.get(reverse('djangoapp:add_review', args=[1]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_add_review_authenticated(self):
        """Test add review page when logged in"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('djangoapp:add_review', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_car_make_model(self):
        """Test CarMake model"""
        self.assertEqual(str(self.car_make), 'Toyota')
        
    def test_car_model_model(self):
        """Test CarModel model"""
        expected = f"{self.car_make.name} {self.car_model.name} ({self.car_model.year})"
        self.assertEqual(str(self.car_model), expected)

    def test_api_endpoints(self):
        """Test API endpoints"""
        # Test dealerships API
        response = self.client.get(reverse('djangoapp:dealerships_api'))
        self.assertEqual(response.status_code, 200)
        
        # Test dealer reviews API
        response = self.client.get(reverse('djangoapp:dealer_reviews_api', args=[1]))
        self.assertEqual(response.status_code, 200)
        
        # Test cars API
        response = self.client.get(reverse('djangoapp:get_cars'))
        self.assertEqual(response.status_code, 200)