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

@catch_errors
def remove_prefix_from_addresses(addresses: list) -> list:
    """
    Function will look for unnecessary words within the address and remove them, keeping strictly the address itself
    :param addresses: list of addresses
    :type addresses: list
    :return: returns the same list with cleaned elements
    """
    def remove_prefix(address: list) -> list:
        pattern = r"[\w\s]*:\s*(.*)"  # Match any prefix followed by zero or more whitespace characters
        address = str(address[0])  # Convert passed argument from a list element to a string
        match = re.search(pattern, address)  # Use regex to find the matched part of the address
        if match:
            return match.group(1).strip()  # Extract the matched part (group 1) and remove leading/trailing whitespace
        else:
            return address  # Return the original address if no match is found
    def remove_commas(address: list) -> list:
        no_comma_address = re.sub(",","",address)
        return no_comma_address
    def remove_non_address(address: list) -> list:
        pattern = re.compile(r"[0-9]+ ([A-Za-z]+( [A-Za-z]+)+) ([A-Za-z0-9]+( [A-Za-z0-9]+)+)",re.IGNORECASE)
        address = str(address[0])  # Convert passed argument from a list element to a string
        match = re.search(pattern, address)  # Use regex to find the matched part of the address
        if match:
            return address  # Extract the matched part (group 1) and remove leading/trailing whitespace
        else:
            pass
    cleansed_addresses = [remove_prefix(address) for address in addresses]
    cleansed_addresses = [remove_commas(address) for address in cleansed_addresses]
    cleansed_addresses = [remove_non_address(address) for address in cleansed_addresses]
    return cleansed_addresses
