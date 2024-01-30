import os
from multiprocessing import cpu_count


host = os.environ.get('TEUTHOLOGY_API_SERVER_HOST', '0.0.0.0')
port = os.environ.get('TEUTHOLOGY_API_SERVER_PORT', '8082')
bind = f'{host}:{port}'
 
workers = cpu_count()
worker_class = 'uvicorn.workers.UvicornWorker'

# loglevel = 'debug'
accesslog = os.path.expanduser("~/teuthology-api.access.log")
# errorlog = os.path.expanduser("~/teuthology-api.error.log") 

