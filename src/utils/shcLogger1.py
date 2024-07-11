import logging
from datetime import datetime
import os

def setup_logging(log_file='shc.log', level=logging.INFO):
    # Ensure the directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        filename=log_file,
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_execution_time(start_time, end_time):
    execution_time_seconds = end_time - start_time
    log_info(f"Execution started at: {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
    log_info(f"Execution finished at: {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")
    log_info(f"Total execution time: {execution_time_seconds:.2f} seconds")
