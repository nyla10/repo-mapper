from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "RepoMapper Engine"
    DEBUG: bool = True
    # Folders we want to ignore when scanning a repo so we don't waste time on junk
    IGNORED_DIRS: set = {
        ".git", "node_modules", "venv", "__pycache__", 
        "dist", "build", ".next", "env", ".env", "target"
    }
    MAX_REPO_SIZE_MB: int = 100

    class Config:
        env_file = ".env"

settings = Settings()