import strawberry
from typing import List
from app.models import Project
from app.database import engine
from ..types import * 
from sqlmodel import Session, select
from app.graphql.queries.project_queries import ProjectQueries

@strawberry.type
class Query(ProjectQueries):
    pass