from rest_framework import serializers
from .models import Doctor,Appointment

from django.contrib.auth.models import User


class Appointmentserializer(serializers.ModelSerializer):

    class Meta:
        model=Appointment
        fields='__all__'

    
    def validate_age(self, value):
        if value < 0:
            raise serializers.ValidationError("Age cannot be negative.")
        return value

    def validate_appointment_date(self, value):
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value


class Doctorserializer(serializers.ModelSerializer):

    class Meta:
        model=Doctor
        fields='__all__'    

class userserializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['username','email','password']
        