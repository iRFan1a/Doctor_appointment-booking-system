from django import forms
from .models import Appointment
from django.contrib.auth.models import User

class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role='doctor'),  # Get only doctors
        empty_label="-- Select a Doctor --",
        widget=forms.Select(attrs={'class': 'form-control'}),
       
    )
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    is_emergency = forms.BooleanField(required=False, label='Emergency Appointment')
    patient = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role='patient'),  # Get only patient
        empty_label="-- Select a Patient --",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-- Age --','style':'height:30px',}),
        label="Age"
    )
    class Meta:
        model = Appointment
        fields = ['patient','age','phone','doctor', 'date','is_emergency']
 
