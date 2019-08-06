from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	tel=models.CharField(max_length=20)
	security=models.CharField(max_length=50)
	def __str__(self):
		return self.user.username