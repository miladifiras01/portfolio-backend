import strawberry
from app.models import *
from sqlmodel import Session, select, delete
from app.database import engine
from .types import *

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_project(self, name: str, description: str, github_url: str | None = None, technologies: list[str] = [], images: list[str] = [], short_description: str = None) -> ProjectType:
        with Session(engine) as session:
            try:
                project = Project(name=name, description=description, github_url =github_url , short_description= short_description)
                session.add(project)
                session.commit()
                session.refresh(project)
                for tech_name in technologies:
                    technology = session.exec(select(Technology).where( Technology.name == tech_name )).first()
                    if not technology:
                        technology = Technology(name=tech_name)
                        session.add(technology)
                        session.flush()
                        session.refresh(technology)
                    project_technology_link = ProjectTechnologyLink(project_id=project.id, technology_id=technology.id)
                    session.add(project_technology_link)
                for image in images:
                    image = ProjectImages(image_url=image, project_id=project.id, created_at=datetime.now())
                    session.add(image)
                    session.flush()
                session.commit()
                session.refresh(project)
                return ProjectType(id=project.id, name=project.name, description=project.description, github_url=project.github_url, technologies=[TechnologyType(id=tech.id, name=tech.name) for tech in project.technologies], images=[ProjectImagesType(id=img.id, image_url=img.image_url) for img in project.images])
            except Exception as e:
                session.rollback()
                raise ValueError(f"Failed to create project: {str(e)}")
    @strawberry.mutation
    def update_project(self, id: int | None = None, name: str | None = None, description: str | None = None, github_url: str | None = None,technologies: list[str] = [], images: list[str] = [], short_description: str = None) -> ProjectType:
        with Session(engine) as session:
            try:
                project = session.get(Project, id)
                if project:
                    project.name = name if name is not None else project.name
                    project.description = description if description is not None else project.description
                    project.github_url = github_url if github_url is not None else project.github_url
                    project.short_description = short_description if short_description is not None else project.short_description
                    session.commit()
                    session.refresh(project)
                    session.exec(delete(ProjectTechnologyLink).where(ProjectTechnologyLink.project_id == project.id))
                    for tech_name in technologies:
                        technology = session.exec(select(Technology).where( Technology.name == tech_name )).first()
                        if not technology:
                            technology = Technology(name=tech_name)
                            session.add(technology)
                            session.flush()
                            session.refresh(technology)
                        project_technology_link = ProjectTechnologyLink(project_id=project.id, technology_id=technology.id)
                        session.add(project_technology_link)
                    session.exec(delete(ProjectImages).where(ProjectImages.project_id == project.id))
                    for image in images:
                        image = ProjectImages(image_url=image, project_id=project.id, created_at=datetime.now())
                        session.add(image)
                        session.flush()
                    session.commit()
                    session.refresh(project)
                    return ProjectType(id=project.id, name=project.name, description=project.description, github_url=project.github_url, technologies=[TechnologyType(id=tech.id, name=tech.name) for tech in project.technologies], images=[ProjectImagesType(id=img.id, project_id=project.id, image_url=img.image_url) for img in project.images], short_description=project.short_description)
                return None
            except Exception as e:
                session.rollback()
                raise ValueError(f"Failed to update project: {str(e)}")
    @strawberry.mutation
    def delete_project(self, id: int) -> bool:
        with Session(engine) as session:
            try:
                project = session.get(Project, id)
                if project:
                    session.exec(delete(ProjectTechnologyLink).where(ProjectTechnologyLink.project_id == project.id))
                    session.delete(project)
                    session.commit()
                    return True
                return False
            except Exception as e:
                session.rollback()
                raise ValueError(f"Failed to delete project: {str(e)}")
    @strawberry.mutation
    def create_technology(self, name: str) -> TechnologyType:  
        with Session(engine) as session:
            try:
                technology = Technology(name=name)
                session.add(technology)
                session.commit()
                session.refresh(technology)
                return TechnologyType(id=technology.id, name=technology.name)
            except Exception as e:
                session.rollback()
                raise ValueError(f"Failed to create technology: {str(e)}")