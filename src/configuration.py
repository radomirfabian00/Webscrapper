import os
import sys


def append_local_packages_to_path(Config: bool = False):
    """
    :param Config: True = Add Python Packages to Path, False = don't
    :type Config: bool
    """
    if Config:
        PY_PACKAGE_LOCATION = os.getenv('LOCALAPPDATA')
        sys.path.append(
            f"{PY_PACKAGE_LOCATION}/Packages/PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0/LocalCache/local-packages/Python312/site-packages")
        print("Appended Python Packages to Path")
        return "Python Package Location Appended to SYS_PATH"
    elif Config is False:
        return None
    else:  # Normally, this exception should NEVER occur, However...
        raise ValueError(f"System Modification Executed without Allowance! Set CONFIG value to False")

    # Defining HEADER will serve as an extra in order to be accepted in websites with raised security


HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
