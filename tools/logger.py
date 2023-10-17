import sys
import logging

def setup_logging():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('BetaLog.log', mode='w')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    class StreamToLogger:
        def __init__(self, logger, log_level=logging.INFO):
            self.logger = logger
            self.log_level = log_level
            self.linebuf = ''

        def write(self, buf):
            self.linebuf += buf
            lines = self.linebuf.split("\n")
            for line in lines[:-1]:
                self.logger.log(self.log_level, line)
            self.linebuf = lines[-1]

        def flush(self):
            pass


# Override sys.stdout to capture print statements
    sys.stdout = StreamToLogger(logger)
