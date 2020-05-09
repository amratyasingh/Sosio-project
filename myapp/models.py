from django.db import models


# Create your models here.
# TODO - move to model after app starts working from views
class Invoice(models.Model):
    name = models.CharField(max_length=100)
