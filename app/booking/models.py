from django.db import models
from django.contrib.auth.models import User
from users.models import Profile

# Create your models here.
class Room(models.Model):
	title = models.CharField(max_length = 100)
	image = models.ImageField(default='conference.webp', upload_to='room_profile_pics')

	def __str__(self):
		return f'{self.title}'


class Meeting(models.Model):
	title = models.CharField(max_length = 100)
	room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='meetings')
	user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='meetings')
	backgroundColor = models.CharField(max_length = 7)
	borderColor = models.CharField(max_length = 7)
	allday = models.BooleanField(default = False)
	isrecurring = models.BooleanField(default = False)
	start = models.DateTimeField()
	end = models.DateTimeField()

	def __str__(self):
		return f'{self.title}'