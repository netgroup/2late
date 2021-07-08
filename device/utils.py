from datetime import datetime
from settings import LOG_FILE_PATH, LOG_FILE_NAME

import logging
import os

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def init_logger():
    """
    Initialise logger
    """
    
    # Create log file directory if it does not exist
    if not os.path.isdir(LOG_FILE_PATH):
        os.mkdir(LOG_FILE_PATH)

    # Get current time
    current_time = datetime.now()

    # Define log file
    log_file = LOG_FILE_PATH + LOG_FILE_NAME + current_time.strftime('%Y_%m_%d')

    # Set logger configuration
    logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s\t[%(levelname)s] %(name)s : %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    return logging.getLogger('2l8')
