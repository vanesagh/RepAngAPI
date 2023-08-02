from django.test import TestCase
from django.db.utils import IntegrityError, DataError
# Create your tests here.
from django.core.exceptions import ValidationError
from raw_materials.models import Brand, Supplier, BrandSupplier
from decimal import Decimal




class BrandSupplierModelTestCase(TestCase):
    def setUp(self):
        # Create some suppliers
        self.supplier_1 = Supplier.objects.create(name="Supplier 1",type="M")
        self.supplier_2 = Supplier.objects.create(name="Supplier 2",type="TA")

        self.brand_1 = Brand.objects.create(name="Brand 1")
        self.brand_2 = Brand.objects.create(name="Brand 2")

    def test_brand_supplier_creation(self):
        brand_supplier = BrandSupplier.objects.create(brand=self.brand_1, supplier=self.supplier_1, offered_price=121.90)
        self.assertTrue(isinstance(brand_supplier, BrandSupplier))
        self.assertTrue(brand_supplier.__str__(), f"{self.brand_1} - {self.supplier_1}")

    def test_brand_supplier_relationship(self):
        brand_supplier = BrandSupplier.objects.create(brand=self.brand_1, supplier=self.supplier_1, offered_price=121.90)

        # Verify that the brand and supplier are associated with BrandSupplier instance
        self.assertEqual(brand_supplier.brand, self.brand_1)
        self.assertEqual(brand_supplier.supplier, self.supplier_1)

        # Verify that the BrandSupplier instance is associated with the brand and supplier
        self.assertIn(brand_supplier, self.brand_1.brandsupplier_set.all())
        self.assertIn(brand_supplier, self.supplier_1.brandsupplier_set.all())

        # Verify that other brand or supplier instances are not associated with BrandSupplier
        self.assertNotIn(brand_supplier, self.brand_2.brandsupplier_set.all())
        self.assertNotIn(brand_supplier, self.supplier_2.brandsupplier_set.all())


class BrandSupplierEdgeTestCase(TestCase):

    def setUp(self):
        self.supplier_1 = Supplier.objects.create(name="Supplier 1", type="M")

        self.brand_1 = Brand.objects.create(name="Brand 1")



    def test_maximum_price_value(self):
        max_price = Decimal('9999999.99')

        with self.assertRaises(DataError):
            BrandSupplier.objects.create(
                brand=self.brand_1,
                supplier=self.supplier_1,
                offered_price=max_price)
