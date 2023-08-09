from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Presentation(models.Model):
    name = models.CharField(max_length=200)
    unique_characteristics = models.JSONField(blank=True, null=True)
    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
