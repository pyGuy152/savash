from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from ..schemas import graphQL_schemas

graphql_router = GraphQLRouter(graphQL_schemas.schema)

router = APIRouter(tags=["GraphQL"])

router.include_router(graphql_router, prefix="/graphql")
