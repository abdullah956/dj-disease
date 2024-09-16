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


class G6PDAssessment(BasedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    family_history = models.BooleanField()  
    close_relatives = models.BooleanField()  
    weakness_fatigue = models.BooleanField()  
    jaundice = models.BooleanField() 
    ethnic_risk = models.BooleanField() 

    def __str__(self):
        return f"Assessment for {self.user.email}"