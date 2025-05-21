import multiprocessing

# Gunicorn configuration file
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 2
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# SSL (if using)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Process naming
proc_name = "taskmanager"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190 