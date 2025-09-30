from django.contrib import admin
from .models import CarMake, CarModel, Dealer, DealerReview


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_make', 'type', 'year']
    list_filter = ['car_make', 'type', 'year']
    search_fields = ['name', 'car_make__name']


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'city', 'state', 'zip']
    list_filter = ['state']
    search_fields = ['full_name', 'city', 'state']


@admin.register(DealerReview)
class DealerReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'dealership', 'car_make', 'car_model', 'sentiment']
    list_filter = ['sentiment', 'purchase', 'car_make']
    search_fields = ['name', 'review']