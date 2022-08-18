import logging
import teuthology.suite
# from teuthology.suite import override_arg_defaults as defaults
# from teuthology.config import config

from fastapi import HTTPException

log = logging.getLogger(__name__)

def run():
    # TODO: hardcoded command_args :P 
    command_args = {
        '--arch': None,
         '--archive-upload': None,
         '--archive-upload-url': None,
         '--ceph': 'wip-dis-testing-2',
         '--ceph-repo': 'https://github.com/ceph/ceph-ci.git',
         '--distro': None,
         '--distro-version': None,
         '--dry-run': False,
         '--email': None,
         '--filter': None,
         '--filter-all': None,
         '--filter-fragments': 'false',
         '--filter-out': None,
         '--flavor': 'default',
         '--force-priority': False,
         '--help': False,
         '--job-threshold': '500',
         '--kernel': 'distro',
         '--limit': '2',
         '--machine-type': 'testnode',
         '--newest': '0',
         '--no-nested-subset': False,
         '--non-interactive': False,
         '--num': '1',
         '--owner': None,
         '--priority': '70',
         '--queue-backend': None,
         '--rerun': None,
         '--rerun-status.': False,
         '--rerun-statuses': 'fail,dead',
         '--rocketchat': None,
         '--seed': '-1',
         '--sha1': None,
         '--sleep-before-teardown': '0',
         '--subset': None,
         '--suite': 'teuthology:no-ceph',
         '--suite-branch': 'wip-dis-testing-2',
         '--suite-dir': None,
         '--suite-relpath': 'qa',
         '--suite-repo': 'https://github.com/ceph/ceph-ci.git',
         '--teuthology-branch': 'main',
         '--throttle': None,
         '--timeout': '43200',
         '--validate-sha1': 'true',
         '--verbose': 1,
         '--wait': False,
         '<config_yaml>': [],
    }
    try:
        teuthology.suite.main(command_args)
        return {"some": "success"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail=repr(exc))
