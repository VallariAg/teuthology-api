import uuid, os
from multiprocessing import Process
import teuthology

def logs_run(func, args):
    """
    Run the command function in a seperate process (to isolate logs),
    and return logs printed during the execution of the function.
    """
    id = str(uuid.uuid4())
    log_file = f'/archive_dir/{id}.log'

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