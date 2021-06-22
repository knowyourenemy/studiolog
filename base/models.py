from django.db import models
from django.urls import path, include
from django.contrib.auth.models import User

# Create your models here.
class Instrument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Piece(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100, null=True, blank=True)
    album = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Practice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    duration = models.DurationField()
    instrument = models.ForeignKey(Instrument, on_delete=models.SET_NULL,null=True, blank=True, related_name='sessions')
    piece = models.ForeignKey(Piece, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.date} for {self.duration}"

    class Meta:
        ordering = ['date']
   





