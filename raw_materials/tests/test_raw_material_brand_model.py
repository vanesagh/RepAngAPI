from django.test import TestCase
from django.db.utils import DataError
from django.core.exceptions import ValidationError
# Create your tests here.
from raw_materials.models import RawMaterial, Brand, RawMaterialBrand


class RawMaterialBrandTestCase(TestCase):
    def setUp(self):
        self.brand_1 = Brand.objects.create(
            name="Test name 1"
        )
        self.brand_2 = Brand.objects.create(
            name="Test name 2"
        )
        self.raw_material = RawMaterial.objects.create(
            product="Test product"
        )

    def test_add_brands_to_raw_materials(self):
        raw_material_brand = RawMaterialBrand.objects.create(
            presentation="Test presentation",
            quantity=36,
            units="ml",
            raw_material=self.raw_material,
            brand=self.brand_1
        )
        self.assertEqual(raw_material_brand.raw_material, self.raw_material)
        self.assertEqual(raw_material_brand.brand, self.brand_1)
        self.assertEqual(raw_material_brand.units, "ml")
        self.assertEqual(raw_material_brand.quantity, 36)
        self.assertEqual(raw_material_brand.presentation, "Test presentation")


""" 
     #def test_valid_units(self):
     #valid_units = ['Kg', 'g', 'L', 'ml', 'Pieza']  
     self.assertIn(self.raw_material.units, valid_units)

    def test_invalid_units_raises_validation_error(self):
        RawMaterial.objects.create(
            product="Test product",
        )



    def test_very_long_presentation(self):
        long_presentation= "Hi"*1000
        with self.assertRaises(DataError):
            RawMaterial.objects.create(
                product="Test product",
            )

    def test_invalid_quantity_value(self):
        invalid_quantity = -5
        with self.assertRaises(ValidationError):
            raw_material = RawMaterial.objects.create(
                product="Test product",
            )
            raw_material.full_clean()
"""
