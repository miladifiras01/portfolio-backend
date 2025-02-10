from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"  # Load variables from the .env file

settings = Settings()  # Create an instance to access values
