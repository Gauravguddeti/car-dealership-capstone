from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DealerReview


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = DealerReview
        fields = ['name', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'review': forms.Textarea(attrs={'rows': 4}),
        }