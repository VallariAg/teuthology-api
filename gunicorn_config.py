import os
from multiprocessing import cpu_count


bind = '0.0.0.0:8082'
 
workers = cpu_count()
worker_class = 'uvicorn.workers.UvicornWorker'

# loglevel = 'debug'
accesslog = os.path.expanduser("~/teuthology-api.access.log")
# errorlog = os.path.expanduser("~/teuthology-api.error.log") 

