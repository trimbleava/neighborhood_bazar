from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    address = models.CharField(max_length=520)
    phone = models.CharField(max_length=11)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)
