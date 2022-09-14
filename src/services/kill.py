import teuthology.kill
from services.helpers import logs_run, github_user_details
import logging, requests # Note: import requests after teuthology


log = logging.getLogger(__name__)


def run(args, send_logs: bool, access_token: str):
    """
    Kill running teuthology jobs.
    """
    try:
        if not access_token:
            raise Exception("No access token. User not authenticated yet to perform this operation.")
        authenticate = github_user_details(access_token, args["--user"])
        if authenticate == True:
            logs = logs_run(teuthology.kill.main, args)
            return { "logs": logs }
        raise Exception(f"Github authentication for user '{args['--user']}' failed.")
    except Exception as exc:
        log.error("teuthology.suite.main failed with the error: " + repr(exc))
        raise