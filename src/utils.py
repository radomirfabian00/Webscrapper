import datetime
import warnings
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_logs_path(dir= 'raw') -> Path:
    if Path(get_project_root() / dir).is_dir():
        return Path(get_project_root() / dir)
    else:
        Path.mkdir(Path(get_project_root() / dir),parents=True,exist_ok=True)
        return Path(get_project_root() / dir)


def get_current_date_hour() -> str:
    return datetime.datetime.now().strftime(r"%Y-%m-%d %H-%M-%S")


def get_filename(logpath,time) -> Path:
    def generate_path_time(logpath,time) -> Path:
        return Path(logpath / time)
    file = Path(f"{generate_path_time(logpath,time)}.txt")
    return file


def catch_errors(function):
    """
    A function wrapper(decorator) to catch all exceptions and print them
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
