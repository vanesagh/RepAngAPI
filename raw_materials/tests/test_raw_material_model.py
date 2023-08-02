from django.test import TestCase
from django.db.utils import DataError,IntegrityError
from django.core.exceptions import ValidationError
# Create your tests here.
from raw_materials.models import RawMaterial, Brand


class RawMaterialModelTest(TestCase):
    def setUp(self):
        # Create some brands
        self.brand_1 = Brand.objects.create(name="Test name 1")
        self.brand_2 = Brand.objects.create(name="Test name 2")

        self.raw_material_1 = RawMaterial.objects.create(product="Test product 1")
        self.raw_material_2 = RawMaterial.objects.create(product="Test product 2")

        # Create RawMaterialBrand instances to associate Brands with RawMaterials
        self.raw_material_brand_1 = self.raw_material_1.rawmaterialbrand_set.create(
            brand=self.brand_1,
            presentation="Presentation 1",
            quantity=1,
            units="L"
        )

        self.raw_material_brand_2 = self.raw_material_2.rawmaterialbrand_set.create(
            brand=self.brand_2,
            presentation="Presentation 2",
            quantity=1,
            units="Kg"
        )

    def test_raw_material_str_representation(self):
        self.assertEqual(str(self.raw_material_1), "Test product 1")

    def test_unique_product(self):
        with self.assertRaises(IntegrityError):
            RawMaterial.objects.create(product="Test product 1")

    def test_raw_material_brand_relationship(self):
        brand = Brand.objects.create(name="Test name")
        raw_material = RawMaterial.objects.create(
            product="Test producto",
        )
        raw_material_brand = raw_material.rawmaterialbrand_set.create(
            brand=brand,
            presentation="Test presentation",
            quantity=1,
            units="kg"
        )

        # Verify that the brand is associated with the raw material
        self.assertIn(raw_material_brand, raw_material.rawmaterialbrand_set.all())

    def test_query_products_by_brand(self):
        # Test case 1: Query products for Brand 1
        products_for_brand_1 = RawMaterial.objects.filter(brands=self.brand_1)
        self.assertIn(self.raw_material_1, products_for_brand_1)
        self.assertNotIn(self.raw_material_2, products_for_brand_1)

        # Test case 2: Query products for Brand 2
        products_for_brand_2 = RawMaterial.objects.filter(brands=self.brand_2)
        self.assertIn(self.raw_material_2, products_for_brand_2)
        self.assertNotIn(self.raw_material_1, products_for_brand_2)

        # Test case 3: Query products for a non-existing brand
        non_existing_brand = Brand(name="Non-existing Brand")
        products_for_non_existing_brand = RawMaterial.objects.filter(brands=non_existing_brand)
        self.assertListEqual(list(products_for_non_existing_brand), [])


    def test_delete_brand_cascade(self):
        raw_material_1_brand_2 = self.raw_material_1.rawmaterialbrand_set.create(
            brand=self.brand_2,
            presentation="Presentation 2",
            quantity=1,
            units="Kg"
        )

        # Verify that the raw material is associated with brands
        self.assertEqual(self.raw_material_1.brands.count(), 2)

        # Delete of the brands
        self.brand_1.delete()

        # Verify that the raw material is no longer associated with the deleted brand
        self.raw_material_1.refresh_from_db()
        self.assertEqual(self.raw_material_1.brands.count(), 1)
        self.assertIn(self.brand_2, self.raw_material_1.brands.all())


class RawMaterialModelEdgeTest(TestCase):
    def test_very_long_product(self):
        long_product = "Hi" * 1000
        with self.assertRaises(DataError):
            RawMaterial.objects.create(product=long_product)

