from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	resturent_name = models.TextField()
	dish = models.TextField()
	price = models.TextField()
	grand_total = models.TextField()
	def __str__(self):
		return f'{self.user.username} Profile'
		