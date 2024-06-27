import logging


def setup_logging():
    # Create a custom logger
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    f_handler = logging.FileHandler('app.log')
    f_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the file handler
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)

    # Add the file handler to the logger
    logger.addHandler(f_handler)

    return logger
