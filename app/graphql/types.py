import strawberry
from sqlmodel import SQLModel
from app.models import Project
from app.models import Technology
from typing import Optional

@strawberry.experimental.pydantic.type(model=Technology, all_fields=True)
class TechnologyType:
    projects: Optional[strawberry.LazyType["ProjectType", __module__]] = None
@strawberry.experimental.pydantic.type(model=Project, all_fields=True)
class ProjectType:
    technologies: Optional[list["TechnologyType"]] = None