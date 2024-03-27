
from typing import TextIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

from configuration import *
from utils import *

LOGS = get_logs_path()
CURRENT_DATE = get_current_date_hour()


@catch_errors
def logger(data) -> TextIO:
    """
    Logging will serve for tracking progress and training regex (manually)
    Could be used to fuel Machine Learning into recognizing addresses,
    As recognizing addresses is the greatest problem currently.

    :type return: Will return location of the file as str object
    """
    file = get_filename()
    with open(file, "w") as file:
        for address in data:
            file.write(address + '\n')
    file.close()
    print(f"Results have been saved to {file}")
    return file


@catch_errors
def grab_info(url) -> TextIO:
    """
    :param url: Input url (must contain https://)
    :type url: link
    :return: Returns the address value scrapped from the url
    :type return: text
    """
    with requests.Session() as session:
        response = session.get(url, headers=HEADER, timeout=(2, 2))
        soup = BeautifulSoup(response.text, "html.parser")
        address_elements = soup.find_all(lambda tag: tag.name == 'p' and 'address' in tag.text.lower()) + \
                           soup.find_all('address') + \
                           soup.find_all(class_=['address', 'vcard', 'contact-text'])
        address = [element.get_text(separator=' ', strip=True) for element in address_elements]
        return address


@catch_errors
def cleanse_addresses(addresses: list) -> list:
    """
    Function will look for unnecessary words within the address and remove them, keeping strictly the address itself
    :param addresses: list of addresses
    :type addresses: list
    :return: returns the same list with cleaned elements
    """
    def remove_prefix(address) -> list:
        pattern = r"[\w\s]*:\s*(.*)"  # Match any prefix followed by zero or more whitespace characters
        address = str(address[0])  # Convert passed argument from a list element to a string
        match = re.search(pattern, address)  # Use regex to find the matched part of the address
        if match:
            return match.group(1).strip()  # Extract the matched part (group 1) and remove leading/trailing whitespace
        else:
            return address  # Return the original address if no match is found

    cleansed_addresses = [remove_prefix(address) for address in addresses]
    return cleansed_addresses

def remove_commas(addresses: list) -> list:
    cleansed_address = []
    for address in addresses:
        cleansed_address.append(re.sub(",","",address))
    return cleansed_address



def remove_non_addresses(addresses: list) -> list:  # TODO
    cleansed_addresses = []
    pattern = r"[0-9]+ ([A-Za-z]+( [A-Za-z]+)+) ([A-Za-z0-9]+( [A-Za-z0-9]+)+)"
    for address in addresses:
        match = re.search(pattern, address)  # Use regex to find the matched part of the address
        if match:
            cleansed_addresses.append(address)
        else:
            pass
    return cleansed_addresses



def main():
    addresses = []  # Initialize addresses as empty array, will be used for storing address values

    df = pd.read_parquet('websites.parquet') # Read addresses from .parquet file
    df = df.head(150) # Uncomment this line to limit the sites that will be scrapped

    # print(df) - Display the .parquet file, uncomment if needed

    # Parse the .parquet file using Pandas (Requires PyArrow, FastParser libraries)
    for _, row in df.iterrows():
        url = "https://" + row['domain']
        address_info = grab_info(url)
        if address_info:
            try:
                print(f"Address info extracted from {url}: {address_info}")
                addresses.append(address_info)
            except Exception as error:
                print(f"Failed to append to addresses: {error}")

    addresses = cleanse_addresses(addresses) # Cleanse address in addresses
    # Cleaning?
    addresses = remove_commas(addresses)
    print(addresses)
    addresses = remove_non_addresses(addresses)
    print(addresses)
    logger(addresses)  # Log addresses into logs folder


if __name__ == "__main__":
    """
    Set CONFIG to True if you have installed libraries and still receive missing libraries error.
    These should normally be set in System Environment Path, however I still had issues even so.
    Fallback Method: 
    Upon getting ImportError, program will wait 10 seconds to confirm Automatic Path Setting. Break out to stop.
    NOTE: The Path Setting is not a permanent change to the system. or at least, I guess so.
    """
    CONFIG = False
    try:
        main()
    except ImportError as e:
        # warnings.warn(f"\n{e}\n")
        print("ImportError detected")
        decision = input("Do you want the program to automatically set it up for you? Y/N: ")
        if decision.lower() in ['y', 'ye', 'yes']:
            CONFIG = True
            append_local_packages_to_path(CONFIG)
        else:
            CONFIG = False
            print("Automatic Setup Canceled")
        print("Resuming execution...")
        main()
