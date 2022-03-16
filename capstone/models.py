from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Places(models.Model):
    place = models.CharField(max_length=50)
    urlPic = models.URLField(max_length=300)
    description = models.TextField(max_length=900)
    
    def __str__(self):
        return f"{self.place}"

class Route(models.Model):
    departure = models.ForeignKey(Places, on_delete=models.CASCADE, related_name="departure")
    destination = models.ForeignKey(Places, on_delete=models.CASCADE, related_name="destination")
    departureDay = models.DateField('day of departure')
    destinationDay = models.DateField('day of arriving')
    departureTime = models.TimeField('time of departure')
    destinationTime = models.TimeField('time of arrival')
    duration = models.TimeField('duration')
    passenger = models.ManyToManyField(User, related_name="passenger")
    

    def serialize(self):
        return {
            "departureTime": self.departureTime,   
        }

    def __str__(self):
        return f"{self.departure} to {self.destination} Departure time: {self.departureDay} [{self.departureTime.strftime('%H:%M')}] Arrival time: {self.destinationDay}[{self.destinationTime.strftime('%H:%M')}] Duration:{self.duration.strftime('%H hours and %M minutes')}"

class Images(models.Model):
    place = models.ForeignKey(Places, on_delete=models.CASCADE, related_name="placePic")
    picture = models.URLField(max_length=300)
    
    def __str__(self):
        return f"{self.place}"


seat_choices= (
    ('A1', 'A1'),
    ('A2', 'A2'),
    ('A3', 'A3'),
    ('A4', 'A4'),
    ('A5', 'A5'),
    ('A6', 'A6'),
    ('B1', 'B1'),
    ('B2', 'B2'),
    ('B3', 'B3'),
    ('B4', 'B4'),
    ('B5', 'B5'),
    ('B6', 'B6'),
)

class Ticket(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="routes")
    seat = models.CharField(max_length=20, blank=True, null=True, choices=seat_choices)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="users")
    price = models.FloatField(default=15)

    def __str__(self):
        return f"{self.seat} for {self.user} Route: {self.route}"

    
