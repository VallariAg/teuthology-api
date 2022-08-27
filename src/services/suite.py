import teuthology.suite
from multiprocessing import Process
import logging, requests, uuid, os # Note: import requests after teuthology
from datetime import datetime

from config import settings

PADDLES_URL = settings.PADDLES_URL

log = logging.getLogger(__name__)


def run(args, dry_run: bool, send_logs: bool):
    """
    Schedule a suite.
    :returns: Run details (dict) and logs (list).
    """
    try:
        args["--timestamp"] = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        if dry_run:
            args['--dry-run'] = True
            logs = logs_run(args)
            return { "run": {}, "logs": logs }

        logs = []
        if send_logs:
            logs = logs_run(args)
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
        raise

def logs_run(args):
    """
    Schedule suite in a seperate process (to isolate logs).
    """
    id = str(uuid.uuid4())
    log_file = f'/archive_dir/{id}.log'

    teuthology_process = Process(target=run_with_logs, args=(args, log_file,))
    teuthology_process.start()
    teuthology_process.join()

    logs = ""
    with open(log_file) as f:
        logs = f.readlines()
    if os.path.isfile(log_file): 
        os.remove(log_file)
    return logs

def run_with_logs(args, log_file):
    """
    Set a new log file to store logs 
    and then schedule suite.
    """
    teuthology.setup_log_file(log_file)
    teuthology.suite.main(args)

def get_run_details(run_name):
    """
    Queries paddles to look if run is created.
    """
    try:
        url = f'{PADDLES_URL}/runs/{run_name}/'
        run_info = requests.get(url).json()
        return run_info
    except:
        raise RuntimeError(f"Unable to find run `{run_name}` in paddles database.")

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
