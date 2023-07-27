from django.contrib import admin

# Register your models here.
from .models import Supplier, RawMaterial, RawMaterialSupplier

admin.site.register(Supplier)
admin.site.register(RawMaterial)
admin.site.register(RawMaterialSupplier)



