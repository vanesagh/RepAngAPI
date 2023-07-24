import json
from django.test import TestCase
from products.schema import schema
from decimal import Decimal as DecimalType
from products.schema import Decimal
from graphql.language import ast

class ProductSchemaValidationTestCase(TestCase):
    def test_validate_graphql_schema(self):
        query = '''
        query IntrospectionQuery {
        __schema {
            types {
                name
                kind
                }
            }
        }
    '''
        result = schema.execute(query)
        assert not result.errors, f"The GraphQL schema is invalid: {result.errors}"

        #response_data = result.data
        #print(json.dumps(response_data,indent=2))

class DecimalTypeTestCase(TestCase):
    def test_parse_value(self):
        # Test with valid input
        input_value = 100.50
        expected_output = DecimalType("100.50")
        self.assertEqual(Decimal.parse_value(input_value),expected_output)

    def test_parse_literal(self):
        # Test with valid FloatValueNode
        float_value_node = ast.FloatValueNode(value="100.95")
        expected_output = DecimalType("100.95")
        self.assertEqual(Decimal.parse_literal(float_value_node),expected_output)

        # Test with invalid node (not a FloatValueNode)
        int_value_node = ast.IntValueNode(value="5")
        self.assertIsNone(Decimal.parse_literal(int_value_node))

        # Test with None node
        self.assertIsNone(Decimal.parse_literal(None))