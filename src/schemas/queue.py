from typing import Union, Optional
from pydantic import Field

from .base import BaseArgs


class QueueArgs(BaseArgs):
    machine_type: Union[str, None] = Field(default='smithi', alias="--machine-type")
    delete: Union[str, None] = Field(default=None, alias="--delete") 
    description: Union[bool, None] = Field(default=None, alias="--description")
    runs: Union[bool, None] = Field(default=None, alias="--runs")
    full: Union[bool, None] = Field(default=False, alias="--full")
    status: Union[bool, None] = Field(default=None, alias="--status")
    pause: Union[int, None] = Field(default=None, alias="--pause")
