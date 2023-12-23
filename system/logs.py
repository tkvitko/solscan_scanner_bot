import logging
import os
from logging import handlers

LOG_DIR = 'logs'
logger = logging.getLogger('scanner')
log_format = logging.Formatter('%(asctime)s %(module)s %(levelname)s %(message)s')
handler = handlers.TimedRotatingFileHandler(filename=os.path.join(LOG_DIR, 'scanner.log'),
                                            when='D',
                                            interval=1,
                                            backupCount=2)
handler.setFormatter(log_format)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
