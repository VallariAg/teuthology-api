from typing import Union
from pydantic import Field

from .base import BaseArgs


class KillArgs(BaseArgs):
    # pylint: disable=too-few-public-methods
    """
    Class for KillArgs.
    """
    owner: Union[str, None] = Field(default=None, alias="--owner")
    run: Union[str, None] = Field(default=None, alias="--run")
    preserve_queue: Union[bool, None] = Field(default=None, alias="--preserve-queue")
    job: Union[list, None] = Field(default=None, alias="--job")
    jobspec: Union[str, None] = Field(default=None, alias="--jobspec")
    machine_type: Union[str, None] = Field(default='default', alias="--machine-type")
    archive: Union[str, None] = Field(default=None, alias="--archive")
