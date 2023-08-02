from django.contrib import admin

# Register your models here.
from .models import Supplier, RawMaterial, Brand, RawMaterialBrand, BrandSupplier
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join, format_html

class RawMaterialBrandInline(admin.TabularInline):
    model = RawMaterialBrand
    extra = 1


class BrandSupplierInline(admin.TabularInline):
    model = BrandSupplier
    extra = 1


class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ['product', 'get_brands_with_suppliers']

    def get_brands_with_suppliers(self, obj):
        brands_with_suppliers = []
        for brand in obj.brands.all():
            suppliers_for_brand = brand.suppliers.all()
            suppliers_info = format_html_join(
                mark_safe('<br>'),
                "{} - {}",
                ((supplier.name, BrandSupplier.objects.get(brand=brand, supplier=supplier).offered_price) for supplier
                 in suppliers_for_brand)
            )
            brands_with_suppliers.append(format_html("{}:<br>{}", brand.name, suppliers_info))
        return mark_safe("<br><br>".join(brands_with_suppliers))

    get_brands_with_suppliers.short_description = "Brands with suppliers"

    inlines = [RawMaterialBrandInline]


class BrandAdmin(admin.ModelAdmin):
    inlines = [BrandSupplierInline]


admin.site.register(Supplier)
admin.site.register(RawMaterial, RawMaterialAdmin)
admin.site.register(Brand, BrandAdmin)

