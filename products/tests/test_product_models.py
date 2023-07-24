from django.test import TestCase
from unittest.mock import patch

# Create your tests here.
from products.models import Product

class ProductModelTest(TestCase):
    @patch('django.db.backends.postgresql.base.DatabaseWrapper.ensure_connection')
    def test_create_product_with_valid_data(self, mock_ensure_connection):
        # Test creating a product with valid data
        product = Product.objects.create(
            name="Test Product",
            description="This is a test product",
            price=100.00,
            category="pan"
        )
        self.assertIsNotNone(product.id)
        self.assertEqual(product.name,"Test Product")
        self.assertEqual(product.description, "This is a test product")
        self.assertEqual(product.price, 100.00)
        self.assertEqual(product.category,"pan")

    def test_create_product_with_invalid_data(self):
        # Test creating a product with invalid data
        with self.assertRaises(Exception):
            Product.objects.create(
                description="This is a test product",
                price=100.00,
                category="invalid_category"

            )


    def test_model_str_representation(self):
        # Create a Product instance
        product = Product.objects.create(
            name="Test Product",
            description="This is a test product",
            price=99.99,
            category="pan"
        )
        # Check if the __str__ method returns the expected representation
        self.assertEqual(str(product),"Test Product")


