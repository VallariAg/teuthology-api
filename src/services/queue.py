import teuthology.suite
from services.helpers import logs_run
import logging, requests # Note: import requests after teuthology
from datetime import datetime

from config import settings

PADDLES_URL = settings.PADDLES_URL

log = logging.getLogger(__name__)


def run(args, delete: str, pause: int):
    """
    List Jobs in queue.

    :param str delete: String defining a PATTERN. 
                       Delete Jobs with PATTERN in their name.
    :param int pause:  Pause queues for a number of seconds. A value of 0
                       will unpause. If -m is passed, pause that queue,
                       otherwise pause all queues.
    """
    try:
        # TODO: does pause and delete have to be query params? 
        # why not simply get it in request body like other params?
        if delete:
            args["--delete"] = delete
        if pause:
            args["pause"] = pause
        results = logs_run(teuthology.beanstalk.main, args)
        return { "results": results }
    except Exception as exc:
        log.error("teuthology.suite.main failed with the error: " + repr(exc))
        raise