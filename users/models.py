from django.contrib.auth.models import AbstractUser
from django.db import models

from config.models import BasedModel

from .managers import UserManager


class User(AbstractUser, BasedModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Contact(BasedModel):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class G6PDAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Family History
    family_history = models.BooleanField()
    close_relatives = models.BooleanField()
    
    # Symptoms After Food or Medication
    weakness_fatigue = models.BooleanField()
    jaundice = models.BooleanField()
    dark_urine = models.BooleanField()
    
    # Exposure to Known Triggers
    eaten_fava_beans = models.BooleanField()
    medication_triggers = models.JSONField()  # List of medications taken
    
    # Geographic and Ethnic Risk Factors
    ethnic_risk = models.BooleanField()
    lived_in_malaria_region = models.BooleanField()
    
    # Symptoms in Infants (If applicable)
    jaundiced_after_birth = models.BooleanField(null=True, blank=True)
    required_phototherapy = models.BooleanField(null=True, blank=True)
    
    def __str__(self):
        return f"Assessment for {self.user.email}"