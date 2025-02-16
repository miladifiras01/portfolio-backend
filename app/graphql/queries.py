import strawberry
from typing import List
from app.models import Project
from app.database import engine
from .types import * 
from sqlmodel import Session, select

@strawberry.type
class Query:
    @strawberry.field
    def get_projects(self) -> List[ProjectType]:
        with Session(engine) as session:
            projects = session.exec(select(Project)).all()  # Fetch all projects
            return [ProjectType(id=p.id, name=p.name, description=p.description, github_url=p.github_url, technologies=[TechnologyType(id=tech.id, name=tech.name) for tech in p.technologies], images=[ProjectImages(image_url=image.image_url) for image in p.images], short_description= p.short_description) for p in projects]

    @strawberry.field
    def get_project(self, id: int) -> ProjectType | None:
        with Session(engine) as session:
            project = session.get(Project,id)
            if project:
                return ProjectType(id=project.id, name=project.name, description=project.description, github_url=project.github_url, technologies=[TechnologyType(id=tech.id, name=tech.name) for tech in project.technologies])
            return None
