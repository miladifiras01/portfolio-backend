import strawberry
from app.models import *
from sqlmodel import Session, select, delete
from app.database import engine
from ..types import *
from app.graphql.mutations.project_mutations import ProjectMutations
from app.graphql.mutations.technology_mutations import TechnologyMutations

@strawberry.type
class Mutation(ProjectMutations, TechnologyMutations):
    pass