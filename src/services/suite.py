from fastapi import HTTPException
from services.helpers import logs_run, get_run_details
from datetime import datetime
from config import settings
import teuthology.suite
import logging

log = logging.getLogger(__name__)


def run(args, dry_run: bool, send_logs: bool, access_token: str):
    """
    Schedule a suite.
    :returns: Run details (dict) and logs (list).
    """
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="You need to be logged in",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        args["--timestamp"] = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        if dry_run:
            args['--dry-run'] = True
            logs = logs_run(teuthology.suite.main, args)
            return { "run": {}, "logs": logs }

        logs = []
        if send_logs:
            logs = logs_run(teuthology.suite.main, args)
        else:
            teuthology.suite.main(args)

        # get run details from paddles
        run_name = make_run_name({
            "machine_type": args["--machine-type"], 
            "user": args["--user"], 
            "timestamp": args["--timestamp"],
            "suite": args["--suite"], 
            "ceph_branch": args["--ceph"],
            "kernel_branch": args["--kernel"], 
            "flavor": args["--flavor"]
        })
        run_details = get_run_details(run_name)
        return { "run": run_details, "logs": logs }
    except Exception as exc:
        log.error("teuthology.suite.main failed with the error: " + repr(exc))
        raise HTTPException(status_code=500, detail=repr(exc))

def make_run_name(run):
    """
    Generate a run name. A run name looks like:
        teuthology-2014-06-23_19:00:37-rados-dumpling-testing-basic-plana
    """
    if "," in run["machine_type"]:
        worker = "multi"
    else:
        worker = run["machine_type"]

    return '-'.join(
        [
            run["user"],
            str(run["timestamp"]),
            run["suite"],
            run["ceph_branch"],
            run["kernel_branch"] or '-',
            run["flavor"], worker
        ]
    ).replace('/', ':')
