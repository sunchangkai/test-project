import logging


class Logger(object):
    def __init__(self, log_name, log_path, log_level=logging.INFO):
        self.path = log_path
        self.log_name = log_name
        self.log_level = log_level
        # create a logger
        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(self.log_level)
        if not self.logger.handlers:
            # create a handler
            fh = logging.FileHandler(self.path)
            self.logger.setLevel(self.log_level)
            # create another handler，to output info in console
            ch = logging.StreamHandler()
            ch.setLevel(self.log_level)
            # define the format of handler
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            # add handler to logger
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def add_log(self, s):
        self.logger.info(s)


if __name__ == "__main__":
    log = Logger("test", "test.log")
    for i in range(5):
        log.add_log(f"i")
