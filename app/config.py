from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """All configuration from environment (.env). Set all variables in .env (see .env.example)."""

    mongodb_url: str = ""
    database_name: str = ""
    jwt_secret: str = ""
    jwt_algorithm: str = ""  # Defaults to HS256 in auth if unset
    jwt_expire_minutes: int = 0
    cors_origins: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}

    def get_cors_origins_list(self) -> list[str]:
        if not self.cors_origins.strip():
            return []
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


def _validate_settings() -> None:
    required = [
        ("MONGODB_URL", settings.mongodb_url),
        ("DATABASE_NAME", settings.database_name),
        ("JWT_SECRET", settings.jwt_secret),
    ]
    missing = [name for name, val in required if not (val and str(val).strip())]
    if missing:
        raise RuntimeError(
            f"Missing required env vars: {', '.join(missing)}. "
            "Copy .env.example to .env and set all values."
        )
    if settings.jwt_expire_minutes <= 0:
        raise RuntimeError("JWT_EXPIRE_MINUTES must be a positive integer in .env")
    if not settings.get_cors_origins_list():
        raise RuntimeError("CORS_ORIGINS must be set in .env (comma-separated origins)")


settings = Settings()
_validate_settings()
