from django.test import TestCase
# Create your tests here.
from raw_materials.models import Supplier
from django.core.exceptions import ValidationError
class SupplierModelTest(TestCase):

    def setUp(self):
        self.valid_supplier_data = {
            "name": "Test name",
            "type": "M",
        }

    def test_create_supplier_with_valid_data(self):
        supplier = Supplier.objects.create(**self.valid_supplier_data)
        self.assertIsNotNone(supplier.id)
        self.assertEqual(supplier.name, "Test name")
        self.assertEqual(supplier.type, "M")

    def test_create_supplier_with_invalid_data(self):
        self.invalid_supplier_data = {
            'name': "Test name",
            'type': "XDF"
        }
        with self.assertRaises(ValidationError):
            supplier = Supplier.objects.create(**self.invalid_supplier_data)
            supplier.full_clean()

    def test_valid_supplier_types(self):
        valid_types = ['TA', 'TL', 'M']
        for type_code, _ in Supplier.TYPES:
            self.assertIn(type_code,valid_types)

    def test_invalid_supplier_type_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            supplier = Supplier.objects.create(name="Test name", type="XFD")
            supplier.full_clean()
    def test_supplier_str_representation(self):
        supplier = Supplier.objects.create(**self.valid_supplier_data)
        self.assertEqual(str(supplier), "Test name")

