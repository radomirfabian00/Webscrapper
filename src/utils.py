import datetime
import warnings
import re
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_logs_path() -> Path:
    return Path(get_project_root() / 'logs')


def get_current_date_hour() -> str:
    return datetime.datetime.now().strftime(r"%Y-%m-%d %H-%M-%S")


def get_filename() -> Path:
    def generate_path_time() -> Path:
        return Path(get_logs_path() / get_current_date_hour())

    file = Path(f"{generate_path_time()}.txt")
    return file


def catch_errors(function):
    """
    A function wrapper to catch all exceptions and print them
    :param function: Your Function
    :type param: func
    :return: Error
    """

    def handler(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            warnings.warn(f"Error in function {(function.__name__).upper()}: {e}")

    return handler
