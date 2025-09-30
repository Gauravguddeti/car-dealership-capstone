from django.db import models
from django.contrib.auth.models import User


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type_choices = [
        ('SUV', 'SUV'),
        ('SEDAN', 'Sedan'),
        ('WAGON', 'Wagon'),
        ('HATCHBACK', 'Hatchback'),
        ('CONVERTIBLE', 'Convertible'),
        ('COUPE', 'Coupe'),
        ('TRUCK', 'Truck'),
    ]
    type = models.CharField(max_length=20, choices=type_choices)
    year_choices = [(i, i) for i in range(2015, 2024)]
    year = models.IntegerField(choices=year_choices)
    
    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"


class Dealer(models.Model):
    """Model representing a car dealer"""
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    st = models.CharField(max_length=10)  # State abbreviation
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)
    lat = models.FloatField()
    long = models.FloatField()
    short_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.full_name


class DealerReview(models.Model):
    """Model representing a dealer review"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    dealership = models.IntegerField()  # Dealer ID
    review = models.TextField()
    purchase = models.BooleanField()
    purchase_date = models.DateField()
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField()
    sentiment = models.CharField(max_length=20, default='neutral')
    
    def __str__(self):
        return f"Review by {self.name} for dealer {self.dealership}"