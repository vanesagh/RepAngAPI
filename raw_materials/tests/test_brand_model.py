from django.test import TestCase
# Create your tests here.
from raw_materials.models import Brand
from django.core.exceptions import ValidationError
from django.db.utils import DataError


class BrandModelTestCase(TestCase):
    def setUp(self):
        self.valid_brand_data = {
            "name": "Test name"
        }

    def test_create_brand_with_valid_data(self):
        brand = Brand.objects.create(**self.valid_brand_data)
        self.assertIsNotNone(brand.id)
        self.assertEqual(brand.name, "Test name")


    def test_create_brand_with_invalid_data(self):
        with self.assertRaises(DataError):
            brand=Brand.objects.create(name="Hi"*1000)
            brand.full_clean()


    def test_brand_str_representation(self):
        brand = Brand.objects.create(**self.valid_brand_data)
        self.assertEqual(str(brand), "Test name")


