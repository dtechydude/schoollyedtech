from django.db import models

# Create your models here.
class SchoolDetail(models.Model):
    name = models.CharField(max_length=150, blank=True)
    slogan = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=150, blank=True)
    email = models.CharField(max_length=150, blank=True)
    website = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f'{self.name}'