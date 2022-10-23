from django.db import models
from auth_module.models import User

class Watchlist(models.Model):
  token = models.CharField(max_length=32, unique=True)
  user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='watchlist')
