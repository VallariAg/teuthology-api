import teuthology
import uuid, os, requests, logging # Note: import requests after teuthology
from multiprocessing import Process
from config import settings


logger = logging.getLogger(__name__)

def logs_run(func, args):
    """
    Run the command function in a seperate process (to isolate logs),
    and return logs printed during the execution of the function.
    """
    id = str(uuid.uuid4())
    log_file = f'/tmp/{id}.log'

    teuthology_process = Process(
        target=_execute_with_logs, args=(func, args, log_file,))
    teuthology_process.start()
    teuthology_process.join()

    logs = ""
    with open(log_file) as f:
        logs = f.readlines()
    if os.path.isfile(log_file): 
        os.remove(log_file)
    return logs

def _execute_with_logs(func, args, log_file):
    """
    To store logs, set a new FileHandler for teuthology root logger
    and then execute the command function.
    """
    teuthology.setup_log_file(log_file)
    func(args)

def github_user_details(access_token: str, username: str):
    team_name = settings.admin_team
    url = f"https://api.github.com/orgs/ceph/teams/{team_name}/memberships/{username}"
    headers = {"Authorization": access_token}

    resp = requests.get(url=url, headers=headers)
    logger.info(resp.json())

    if resp.status_code == 200:
        return True
    return resp.json()
