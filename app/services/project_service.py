from sqlmodel import Session, select, delete
from app.database import engine
from app.models import *
from app.graphql.types import *

def create_project(name: str, description: str = "", github_url: str | None = None, technologies: list[str] = [], images: list[str] = [], short_description: str = None):
    with Session(engine) as session:
        try:
            project = Project(name=name, description=description, github_url =github_url , short_description= short_description)
            session.add(project)
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
            return ProjectType(id=project.id, name=project.name, description=project.description, github_url=project.github_url, technologies=[TechnologyType(id=tech.id, name=tech.name) for tech in project.technologies], images=[ProjectImagesType(id=img.id, image_url=img.image_url, project_id=img.project_id) for img in project.images])
        except Exception as e:
            session.rollback()
            raise ValueError(f"Failed to create project: {str(e)}")

def update_project(id: int, name: str | None = None, description: str | None = None, github_url: str | None = None, technologies: list[str] = [], images: list[str] = [], short_description: str = None):
    with Session(engine) as session:
        try:
            project = session.get(Project, id)
            if project:
                project.name = name if name is not None else project.name
                project.description = description if description is not None else project.description
                project.github_url = github_url if github_url is not None else project.github_url
                project.short_description = short_description if short_description is not None else project.short_description
                if len(technologies) > 0:
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
                if len(images) > 0:
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

def delete_project(id: int):
    with Session(engine) as session:
        try:
            project = session.get(Project, id)
            if project:
                session.exec(delete(ProjectTechnologyLink).where(ProjectTechnologyLink.project_id == project.id))
                session.exec(delete(ProjectImages).where(ProjectImages.project_id == project.id))
                session.delete(project)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise ValueError(f"Failed to delete project: {str(e)}")


def get_projects():
    with Session(engine) as session:
        projects = session.exec(select(Project)).all()
        return [
            ProjectType(
                id=p.id, 
                name=p.name, 
                description=p.description, 
                github_url=p.github_url, 
                technologies=[
                    TechnologyType(id=tech.id, name=tech.name) for tech in p.technologies
                ],
                images=[
                    ProjectImages(image_url=image.image_url) for image in p.images
                ],
                short_description=p.short_description
            ) for p in projects
        ]

def get_project(id: int):
    with Session(engine) as session:
        project = session.get(Project, id)
        if project:
            return ProjectType(
                id=project.id, 
                name=project.name, 
                description=project.description, 
                github_url=project.github_url, 
                technologies=[
                    TechnologyType(id=tech.id, name=tech.name) for tech in project.technologies
                ],
                images=[ProjectImages(image_url=image.image_url) for image in project.images],
                short_description= project.short_description
            )
        return None
def get_project_by_column(column: str, value: str) -> ProjectType | None: 
    with Session(engine) as session:
        project = session.exec(select(Project).where(getattr(Project, column) == value)).first()
        if project:
            return ProjectType(
                id=project.id, 
                name=project.name, 
                description=project.description, 
                github_url=project.github_url, 
                technologies=[
                    TechnologyType(id=tech.id, name=tech.name) for tech in project.technologies
                ],
                images=[ProjectImages(image_url=image.image_url) for image in project.images],
                short_description= project.short_description
            )
        return None
def update_images(id: int, images: list[str]):
    with Session(engine) as session:
        try:
            project = session.get(Project, id)
            if project:
                existing_images = {img.image_url for img in project.images}
                new_images = set(images)
                images_to_remove = existing_images - new_images
                for image_url in images_to_remove:
                    session.exec(delete(ProjectImages).where(ProjectImages.project_id == project.id, ProjectImages.image_url == image_url))
                images_to_add = new_images - existing_images
                for image_url in images_to_add:
                    new_image = ProjectImages(image_url=image_url, project_id=project.id, created_at=datetime.now())
                    session.add(new_image)

                session.commit()
                session.refresh(project)
                return ProjectType(id=project.id, name=project.name, description=project.description, github_url=project.github_url, technologies=[TechnologyType(id=tech.id, name=tech.name) for tech in project.technologies], images=[ProjectImagesType(id=img.id, project_id=project.id, image_url=img.image_url) for img in project.images], short_description=project.short_description)
            return None
        except Exception as e:
            session.rollback()
            raise ValueError(f"Failed to update project: {str(e)}")