from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORIES = [
        ('pan','Pan'),
        ('pastel','Pastel'),
        ('galletas','Galletas'),
        ('pays','Pays'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORIES,null=True)


    def __str__(self):
        return self.name


