import pathlib
import logging
import logging.handlers


def init_logger(log_dirname):
    logging.basicConfig(level=logging.NOTSET)
    pathlib.Path('./logs/{}'.format(log_dirname))\
        .mkdir(parents=True, exist_ok=True)


def set_thread_logger(log_dirname, thread_name):
    logger = logging.getLogger('[Thread-{}]'.format(thread_name))
    logformatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    access_handler = logging.handlers.RotatingFileHandler(
            './logs/{}/access.log'.format(log_dirname),
            maxBytes=10**8,
            backupCount=5
            )
    access_handler.setFormatter(logformatter)
    access_handler.setLevel(logging.INFO)
    logger.addHandler(access_handler)

    error_handler = logging.handlers.RotatingFileHandler(
            './logs/{}/error.log'.format(log_dirname),
            maxBytes=10**8,
            backupCount=5
            )
    error_handler.setFormatter(logformatter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

    return logger


