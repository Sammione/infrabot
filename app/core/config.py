from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    app_name: str = "LMS Chatbot API"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    lms_base_url: str = os.getenv("LMS_BASE_URL", "")
    lms_api_key: str = os.getenv("LMS_API_KEY", "")
    lms_tenant_key: str = os.getenv("LMS_TENANT_KEY", "infracredit")
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
