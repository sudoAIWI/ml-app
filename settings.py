from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, Field
from typing import Optional
import yaml
import os


class Settings(BaseSettings):
    ENVIRONMENT: str
    APP_NAME: str
    API_KEY: Optional[str] = Field(default=None)
    DATABASE_URL: Optional[str] = Field(default=None)

    model_config = SettingsConfigDict(env_file=".env.test", extra="ignore")

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, value):
        valid_environments = {"dev", "test", "prod"}
        if value not in valid_environments:
            raise ValueError(
                f"Environment must be one of {valid_environments}, got '{value}'"
            )
        return value

    @classmethod
    def load_secrets(cls):
        """Load secrets from encrypted YAML file"""
        secrets_file = "secrets.yaml"
        if os.path.exists(secrets_file):
            try:
                with open(secrets_file, "r") as f:
                    secrets = yaml.safe_load(f)
                    for key, value in secrets.items():
                        os.environ[key] = str(value)
            except Exception as e:
                print(f"Warning: Could not load secrets: {e}")
