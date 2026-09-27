from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # LLM Provider
    llm_api_key: str = ""
    llm_base_url: str = "https://openrouter.ai/api/v1"
    
    # We use a cheaper model for workers, stronger for orchestrator
    orchestrator_model: str = "google/gemini-pro-1.5"
    worker_model: str = "google/gemini-flash-1.5"
    
    # Optional tools
    tavily_api_key: str = "" # For web search
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
