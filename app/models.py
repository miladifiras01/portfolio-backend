from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class ProjectTechnologyLink(SQLModel, table=True):
    project_id: Optional[int] = Field(default=None, foreign_key="project.id", primary_key=True)
    technology_id: Optional[int] = Field(default=None, foreign_key="technology.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    short_description: Optional[str] = None 
    role: Optional[str] = None
    impact: Optional[str] = None
    github_url: Optional[str] = None
    technologies: List["Technology"] = Relationship(
        back_populates="projects",
        link_model=ProjectTechnologyLink
    )
    images: List["ProjectImages"] = Relationship(back_populates="project")
    created_at: datetime = Field(default_factory=datetime.now)

class Technology(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    projects: List[Project] = Relationship(back_populates="technologies", link_model=ProjectTechnologyLink)
    created_at: datetime | None = Field(default_factory=datetime.now)

class ProjectImages(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    image_url: str
    created_at: datetime = Field(default_factory=datetime.now)
    project: Project = Relationship(back_populates="images")