from sqlmodel import Session
from app.database import engine
from app.models import Technology
from app.graphql.types import TechnologyType

def create_technology(name: str):
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
