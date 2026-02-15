from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    gemini_api_key: str
    pdfshift_api_key: str
    
    # App Settings
    app_name: str = "CV Generator API"
    debug: bool = True

    model_config = SettingsConfigDict(env_file=".env")


def get_settings():
    return Settings()
