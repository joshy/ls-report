"""
Module to run the application. Defines also logging configuration.
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler

def configure(app):
    """
    Setups up logging.
    """
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    log_file = os.path.join(log_dir, 'server.log')

    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    handler = TimedRotatingFileHandler(log_file, when='midnight', backupCount=10)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    app.logger.addHandler(handler)
