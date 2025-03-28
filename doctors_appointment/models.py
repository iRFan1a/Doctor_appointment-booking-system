from django.db import models
from django.contrib.auth.models import User

# Create your models here.




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = [('patient', 'Patient'), ('doctor', 'Doctor')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    image=models.ImageField(upload_to='profilepic',default='media/profilepic/default.jpg')
    

    def __str__(self):
        return f"{self.user.username} ({self.role})"




class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    specialization = models.CharField(max_length=100)
    availability = models.CharField(max_length=50) 
    image=models.ImageField(upload_to='doctorpic',default=1)
    

    def __str__(self):
        return f"{self.name} - {self.specialization}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    patient =models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments",default=1)
    age = models.IntegerField()
    phone=models.CharField(max_length=10,default=1)
    doctor =models.ForeignKey(User, on_delete=models.CASCADE, related_name="patients",default=1)
    date = models.DateTimeField()
    is_emergency = models.BooleanField(default=False)  # Emergency flag
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
   
    def __str__(self):
        return f"Appointment with {self.patient.username} {self.doctor.username} on {self.date}"    



