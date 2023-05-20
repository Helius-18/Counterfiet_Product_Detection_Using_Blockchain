from django.db import models
from django.contrib.auth.models import User

class Manufacturer(models.Model):
    manufacturer_ID = models.CharField(max_length=50)
    # other fields...
    
class Retailer(models.Model):
    retailer_ID = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    # other fields...

class ManufacturerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manufacturer = models.OneToOneField(Manufacturer, on_delete=models.CASCADE)

class RetailerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    retailer = models.OneToOneField(Retailer, on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=255, unique=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Block(models.Model):
    previous_block = models.CharField(max_length=255)
    current_block = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.current_block