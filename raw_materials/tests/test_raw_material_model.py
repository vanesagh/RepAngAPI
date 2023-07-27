from django.test import TestCase
from django.db.utils import DataError
from django.core.exceptions import ValidationError
# Create your tests here.
from raw_materials.models import RawMaterial, Supplier


class RawMaterialModelTest(TestCase):
    def setUp(self):

        # Create some suppliers
        self.supplier_1 = Supplier.objects.create(
            name="Test name",
            type="M"
        )
        self.supplier_2 = Supplier.objects.create(
            name="Test name",
            type="TL"
        )

        self.raw_material = RawMaterial.objects.create(
            product="Test product",
            brand="x",
            presentation="",
            quantity=44,
            units="Kg"
        )

    def test_raw_material_str_representation(self):
        self.assertEqual(str(self.raw_material), "Test product")

    def test_raw_material_supplier_relationship(self):
        supplier = Supplier.objects.create(name="Test name", type='TA')
        raw_material = RawMaterial.objects.create(
            product="Test producto",
            brand="x",
            presentation="",
            quantity=44,
            units="L"
        )

        raw_material.suppliers.add(supplier, through_defaults={'offered_price': 90})
        # Verify that the supplier is associated with the raw material
        self.assertIn(supplier, raw_material.suppliers.all())

    def test_query_products_by_supplier(self):
        supplier_1 = Supplier.objects.create(name="La Comer", type='TA')
        supplier_2 = Supplier.objects.create(name="Mercado Coyoacan", type='M')
        raw_material_1 = RawMaterial.objects.create(
            product="Test product1",
            brand="x",
            presentation="",
            quantity=44,
            units="ml"
        )
        raw_material_2 = RawMaterial.objects.create(
            product="Test product2",
            brand="x",
            presentation="p",
            quantity=44,
            units="g"
        )
        raw_material_1.suppliers.add(supplier_1, through_defaults={'offered_price': 50})

        raw_materials_by_supplier_1 = RawMaterial.objects.filter(suppliers=supplier_1)
        self.assertEqual(list(raw_materials_by_supplier_1), [raw_material_1])

        raw_material_2.suppliers.add(supplier_2, through_defaults={'offered_price': 450})

        raw_materials_by_supplier_2 = RawMaterial.objects.filter(suppliers=supplier_2)
        self.assertEqual(list(raw_materials_by_supplier_2), [raw_material_2])

    def test_delete_supplier_cascade(self):
        self.raw_material.suppliers.add(self.supplier_1, through_defaults={'offered_price': 150})
        self.raw_material.suppliers.add(self.supplier_2, through_defaults={'offered_price': 100})

        # Verify that the raw material is associated with suppliers
        self.assertEqual(self.raw_material.suppliers.count(), 2)

        # Delete of the suppliers
        self.supplier_1.delete()

        # Verify that the raw material is no longer associated with the deleted supplier
        self.raw_material.refresh_from_db()
        self.assertEqual(self.raw_material.suppliers.count(), 1)
        self.assertIn(self.supplier_2, self.raw_material.suppliers.all())

    def test_valid_units(self):
        valid_units = ['Kg', 'g', 'L', 'ml', 'Pieza']
        self.assertIn(self.raw_material.units, valid_units)

    def test_invalid_units_raises_validation_error(self):
        RawMaterial.objects.create(
            product="Test product",
            brand="Test brand",
            presentation="Test presentation",
            quantity=1,
            units="Invalid",
        )


class RawMaterialModelEdgeTest(TestCase):
    def test_very_long_presentation(self):
        long_presentation= "Hi"*1000
        with self.assertRaises(DataError):
            RawMaterial.objects.create(
                product="Test product",
                brand="Test brand",
                presentation=long_presentation,
                quantity=34,
                units="Kg"
            )

    def test_invalid_quantity_value(self):
        invalid_quantity = -5
        with self.assertRaises(ValidationError):
            raw_material = RawMaterial.objects.create(
                product="Test product",
                brand="Test Brand",
                presentation="Test presentation",
                quantity=invalid_quantity,
                units="ml"
            )
            raw_material.full_clean()


