from django.db import models

# Create your models here.

class Info(models.Model):
  title=models.CharField(max_length=100)
  time=models.CharField(max_length=50)
  content=models.CharField(max_length=15000)
  
  def __str__(self):
    return self.title

