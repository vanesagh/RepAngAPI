from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db import models


# Create your models here.

class Supplier(models.Model):
    TYPES = [
        ('TA', 'Tienda de Autoservicio'),
        ('TL', 'Tienda local'),
        ('M', 'Mercado')
    ]
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=3, choices=TYPES, null=True)

    def __str__(self):
        return self.name


class RawMaterial(models.Model):
    product = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    presentation = models.CharField(max_length=200)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    units = models.CharField(max_length=10)
    suppliers = models.ManyToManyField(Supplier, through='RawMaterialSupplier')

    def __str__(self):
        return self.product





class RawMaterialSupplier(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    offered_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    purchased_date = models.DateField(null=True, default=timezone.now)

    class Meta:
        unique_together = ['raw_material', 'supplier']

    def __str__(self):
        return f"{self.raw_material} - {self.supplier}"


