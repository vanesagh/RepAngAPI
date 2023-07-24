import graphene
from decimal import Decimal as DecimalType
from graphene_django import DjangoObjectType
from graphene.types.scalars import Scalar
from graphql.language import ast
from .models import Product


class Decimal(Scalar):
    @staticmethod
    def serialize(decimal):

        assert isinstance(
            decimal, DecimalType
        ), f'Received not compatible Decimal "{repr(decimal)}"'
        return float(decimal)

    @staticmethod
    def parse_value(value):
        return DecimalType(value)

    @staticmethod
    def parse_literal(node, _variables=None):
        if isinstance(node, ast.FloatValueNode):
            return DecimalType(node.value)
        return None



class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"

    category = graphene.String()
    price = Decimal()

class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.Int())

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_product(self, info, id):
        return Product.objects.get(pk=id)


schema = graphene.Schema(query=Query, types=[Decimal])
