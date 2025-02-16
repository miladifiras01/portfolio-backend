import strawberry
from sqlmodel import SQLModel
from app.models import *
from typing import Optional

@strawberry.experimental.pydantic.type(model=Technology, all_fields=True)
class TechnologyType:
    projects: Optional[strawberry.LazyType["ProjectType", __module__]] = None
@strawberry.experimental.pydantic.type(model=Project, all_fields=True)
class ProjectType:
    technologies: Optional[list["TechnologyType"]] = None
    images: Optional[list[strawberry.LazyType["ProjectImagesType", __module__]]] = None
@strawberry.experimental.pydantic.type(model=ProjectImages, all_fields=True)
class ProjectImagesType:
    project: Optional[ProjectType] = None