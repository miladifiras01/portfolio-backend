# Portfolio Backend

This project is built to make the portfolio more dynamic by handling the CRUD operations for projects in the portfolio's frontend.

## Tech Stack

- **FastAPI**: Backend framework for building APIs
- **GraphQL (Strawberry)**: GraphQL integration for FastAPI
- **PostgreSQL**: Database for storing project data
- **SQLModel**: ORM for database interactions
- **Alembic**: Database migration management

## Features

- Create, update, delete, and fetch projects dynamically
- Handle project technologies and relationships
- Automate project creation by listening to GitHub repository events(upcoming feature):
    - Listens for repository creation events.
    - Adds projects dynamically to the portfolio based on a special topic specified in the repository configuration in GitHub.
## Setup

**Run migrations**:
    ```sh
    alembic revision --autogenerate -m "migration description" #--autogenrate to auto detect changes
    alembic upgrade head
    ```

**Start the FastAPI server**:
    ```sh
    uvicorn app.main:app --reload
    ```

## Future Enhancements

- **Automation**: Add automation to listen for repository creation events in GitHub and add projects dynamically to the portfolio based on a special topic specified in the repository config in GitHub.
