import strawberry
from .queries.queries import Query
from .mutations.mutations import Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)
