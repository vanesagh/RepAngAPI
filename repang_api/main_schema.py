import graphene
from products.schema import Query as QueryApi
from graphene import Schema


class Query(QueryApi, graphene.ObjectType):
    pass


schema = Schema(query=Query)
