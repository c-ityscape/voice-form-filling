import multiprocessing

# Server socket
bind = "0.0.0.0:10000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count()
worker_class = 'sync'
worker_connections = 1000
timeout = 300  # 5 minutes
keepalive = 2

# Process naming
proc_name = 'gunicorn_whisper'

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Maximum size of HTTP request line in bytes
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190