import strawberry
from typing import List
from app.services.project_service import get_projects, get_project
from ..types import ProjectType

@strawberry.type
class ProjectQueries:
    @strawberry.field
    def get_projects(self) -> List[ProjectType]:
        return get_projects()

    @strawberry.field
    def get_project(self, id: int) -> ProjectType | None:
        return get_project(id)
