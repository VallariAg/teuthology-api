from functools import lru_cache
from pydantic import BaseSettings


class APISettings(BaseSettings):
    """
    Class for API settings.
    """

    PADDLES_URL: str = "http://paddles:8080"
    # TODO: team names need to be changed below when created
    admin_team: str = "ceph"  # ceph's github team with *sudo* access to sepia
    teuth_team: str = "teuth"  # ceph's github team with access to sepia

    class Config:
        """
        Class for Config.
        """

        # pylint: disable=too-few-public-methods
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_api_settings() -> APISettings:
    """
    Returns the API settings.
    """
    return APISettings()  # reads variables from environment


settings = get_api_settings()
