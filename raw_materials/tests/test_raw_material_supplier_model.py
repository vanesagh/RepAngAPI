from django.test import TestCase
from django.db.utils import IntegrityError, DataError
# Create your tests here.
from django.core.exceptions import ValidationError
from raw_materials.models import RawMaterial, Supplier, RawMaterialSupplier
from decimal import Decimal




class RawMaterialSupplierTestCase(TestCase):
    def setUp(self):
        # Create some suppliers
        self.supplier_1 = Supplier.objects.create(
            name="Supplier 1",
            type="M"
        )
        self.supplier_2 = Supplier.objects.create(
            name="Supplier 2",
            type="TA"
        )

        # Create a raw material item
        self.raw_material = RawMaterial.objects.create(
            product="Raw Material 1",
            brand="Brand 1",
            presentation="Presentation 1",
            quantity=1,
            units="Kg"
        )

    def test_add_suppliers_to_raw_material(self):
        # Add the supplier to the raw material and provide offered price
        raw_material_supplier = RawMaterialSupplier.objects.create(
            raw_material=self.raw_material,
            supplier=self.supplier_1,
            offered_price=25)

        self.assertEqual(raw_material_supplier.raw_material, self.raw_material)
        self.assertEqual(raw_material_supplier.supplier, self.supplier_1)
        self.assertEqual(raw_material_supplier.offered_price, 25)

    def test_add_duplicate_suppliers_raises_validation_error(self):
        supplier_1 = Supplier.objects.create(name="Supplier 1", type='M')
        supplier_2 = Supplier.objects.create(name="Supplier 2", type='TA')

        # Create a raw material item
        raw_material = RawMaterial.objects.create(
            product="Raw Material 1",
            brand="Brand 1",
            presentation="Presentation 1",
            quantity=1,
            units="Kg"
        )

        # Add the first supplier to the raw material
        RawMaterialSupplier.objects.create(
            raw_material=raw_material,
            supplier=supplier_1,
            offered_price=45
        )

        # Attempting to create a duplicate RawMaterialSupplier
        with self.assertRaises(IntegrityError):
            RawMaterialSupplier.objects.create(
                raw_material=raw_material,
                supplier=supplier_1,
                offered_price=45
            )


class RawMaterialSupplierEdgeTestCase(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Supplier 1",
            type="M"
        )
    def test_maximum_price_value(self):
        max_price = Decimal('9999999.99')
        raw_material = RawMaterial.objects.create(
            product="Raw Material 1",
            brand="Brand 1",
            presentation="Presentation 1",
            quantity=1,
            units="Kg"
        )
        with self.assertRaises(DataError):
            RawMaterialSupplier.objects.create(
                raw_material=raw_material,
                supplier=self.supplier,
                offered_price=max_price

            )
