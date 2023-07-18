from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # Add any additional fields here, such as a profile picture or user type
    pass
