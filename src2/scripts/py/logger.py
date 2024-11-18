import os
import datetime

def setup_logging():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = "./scripts/logs"
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, f"dir_scan_{timestamp}.log")

def log_message(file, message):
    print(message)
    with open(file, 'a') as f:
        f.write(f"{message}\n")
