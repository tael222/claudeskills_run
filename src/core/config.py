"""Application configuration management."""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Claude API
    anthropic_api_key: str = Field(..., description="Anthropic API key")

    # Database
    database_url: str = Field(
        default="sqlite:///./claudeskills.db",
        description="Database connection URL",
    )

    # API Settings
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_reload: bool = Field(default=True, description="API reload on change")

    # Frontend
    frontend_url: str = Field(
        default="http://localhost:3000",
        description="Frontend URL for CORS",
    )

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(default="logs/app.log", description="Log file path")

    # Skills
    skills_dir: Path = Field(default=Path("./skills"), description="Skills directory")
    custom_skills_dir: Optional[Path] = Field(
        default=None,
        description="Custom skills directory (e.g., ~/.claude/skills)",
    )

    # Application
    app_name: str = Field(default="Claude Skills Run", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")

    @property
    def cors_origins(self) -> list[str]:
        """Get CORS origins."""
        return [
            self.frontend_url,
            "http://localhost:3000",
            "http://localhost:5173",  # Vite default
        ]


# Global settings instance
settings = Settings()
