from typing import Union, Optional
from pydantic import Field

from .base import BaseArgs


class SchedulerArgs(BaseArgs):
    owner: Union[str, None] = Field(default=None, alias="--owner")
    num: Union[str, None] = Field(default='1', alias="--num")
    priority: Union[str, None] = Field(default='70', alias="--priority")
    queue_backend: Union[str, None] = Field(default=None, alias="--queue-backend")
    rerun: Union[str, None] = Field(default=None, alias="--rerun")
    seed: Union[str, None] = Field(default='-1', alias="--seed")
    force_priority: Union[bool, None] = Field(default=False, alias="--force-priority")
    no_nested_subset: Union[bool, None] = Field(default=False, alias="--no-nested-subset")
    job_threshold: Union[str, None] = Field(default='500', alias="--job-threshold")
    archive_upload: Union[str, None] = Field(default=None, alias="--archive-upload")
    archive_upload_url: Union[str, None] = Field(default=None, alias="--archive-upload-url")
    throttle: Union[str, None] = Field(default=None, alias="--throttle")
    filter: Union[str, None] = Field(default=None, alias="--filter")
    filter_out: Union[str, None] = Field(default=None, alias="--filter-out")
    filter_all: Union[str, None] = Field(default=None, alias="--filter-all")
    filte_fragments: Union[str, None] = Field(default='false', alias="--filter-fragments")
    subset: Union[str, None] = Field(default=None, alias="--subset")
    timeout: Union[str, None] = Field(default='43200', alias="--timeout")
    rocketchat: Union[str, None] = Field(default=None, alias="--rocketchat")
    limit: Union[str, None] = Field(default='0', alias="--limit")
