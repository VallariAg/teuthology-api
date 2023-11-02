from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    """
    Class for API settings.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    # TODO: team names need to be changed below when created
    admin_team: str = "ceph"  # ceph's github team with *sudo* access to sepia
    teuth_team: str = "teuth"  # ceph's github team with access to sepia


@lru_cache()
def get_api_settings() -> APISettings:
    """
    Returns the API settings.
    """
    return APISettings()  # reads variables from environment


settings = get_api_settings()
