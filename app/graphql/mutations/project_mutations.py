import strawberry
from app.services.project_service import create_project, update_project, delete_project
from app.graphql.types import ProjectType

@strawberry.type
class ProjectMutations:
    @strawberry.mutation
    def create_project(self, name: str, description: str, github_url: str | None = None, technologies: list[str] = [], images: list[str] = [], short_description: str = None) -> ProjectType:
        return create_project(name, description, github_url, technologies, images, short_description)

    @strawberry.mutation
    def update_project(self, id: int, name: str | None = None, description: str | None = None, github_url: str | None = None, technologies: list[str] = [], images: list[str] = [], short_description: str = None) -> ProjectType:
        return update_project(id, name, description, github_url, technologies, images, short_description)

    @strawberry.mutation
    def delete_project(self, id: int) -> bool:
        return delete_project(id)
