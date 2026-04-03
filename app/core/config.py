from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Evidexus Mobile API"
    API_V1_STR: str = "/api/v1"
    
    # Model APIs
    OPENAI_API_KEY: str = ""
    
    # Internal Security
    API_KEY: str = "evidexus_mobile_dev_key"
    
    class Config:
        env_file = ".env"

settings = Settings()
