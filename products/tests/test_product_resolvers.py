from django.test import TestCase
from graphene.test import Client
from products.schema import schema
from products.models import Product

class ResolverTestCase(TestCase):

    def setUp(self):
        # Set up the GraphQL client
        self.graphql_client = Client(schema)

        # Create some test products
        self.product1 = Product.objects.create(
            name="Product 1",
            description="Description 1",
            category="pastel",
            price=99.99)
        self.product2 = Product.objects.create(
            name="Product 2",
            description="Description 2",
            category="pan",
            price=149.99)

    def test_resolve_all_products(self):
        self.maxDiff = None
        # Prepare the GraphQL query
        query = '''
            query getAllProducts {
                allProducts {
                    id
                    name
                    description
                    price
                    category
                }
            }        
        '''

        # Execute the query
        result = self.graphql_client.execute(query)

        # Check the result
        self.assertEqual(result,
                         {
                             'data': {
                                 'allProducts': [
                                     {'id': str(self.product1.id),
                                      'name': self.product1.name,
                                      'description': self.product1.description,
                                      'price': self.product1.price,
                                      'category': self.product1.category,
                                      },
                                     {'id': str(self.product2.id),
                                      'name': self.product2.name,
                                      'description': self.product2.description,
                                      'price': self.product2.price,
                                      'category': self.product2.category,
                                      },
                                 ]

                             }
                         })

    def test_resolve_product(self):
        # Prepare the Graphql query with the product ID of product2
        product_id = self.product2.id
        query = f'''
            query getProductById {{
                product(id:{product_id}){{
                    id
                    name
                    description
                    price
                }}       
            }}
        '''

        # Execute the query
        result = self.graphql_client.execute(query)

        # Check the result
        expected_result = {
            'data': {
                'product': {
                    'id': str(self.product2.id),
                    'name': self.product2.name,
                    'description': self.product2.description,
                    'price': self.product2.price

                }
            }
        }
        self.assertEqual(result, expected_result)
