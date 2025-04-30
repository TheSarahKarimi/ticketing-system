from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    id = models.AutoField (primary_key=True)
    first_name = models.CharField (max_length=255)
    last_name = models.CharField (max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField (
        max_length=255, 
        unique=True, 
        null=True, 
        blank=True,
        validators=[MinLengthValidator(11),MaxLengthValidator(11)])

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.fullname
    
    class Meta:
        ordering = ['id']    