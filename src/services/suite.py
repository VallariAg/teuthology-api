import logging
import teuthology.suite


log = logging.getLogger(__name__)

def run(args):
    try:
        results = teuthology.suite.main(args)
        log.debug(results)
        return
    except Exception as exc:
        log.error("teuthology.suite.main failed with the error: " + repr(exc))
        raise
