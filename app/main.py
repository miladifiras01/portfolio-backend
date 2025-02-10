# app/main.py
from fastapi import FastAPI
from app.database import engine
from sqlmodel import SQLModel
from app.graphql.schema import schema
from strawberry.fastapi import GraphQLRouter
from .models import Project
from .models import Technology
from .models import ProjectTechnologyLink
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now, you can specify specific origins here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, you can restrict it to just GET, POST, etc.
)
    
@app.get("/")
def read_root():
    return {"message": "Database connected with SQLModel!"}

# Add GraphQL router
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")