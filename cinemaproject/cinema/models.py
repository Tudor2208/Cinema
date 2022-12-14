from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.CharField(max_length=30)
    text = models.CharField(max_length=250)
    send_date = models.DateField(auto_now_add=True, auto_now=False)
    response = models.CharField(max_length=250, default = "none")