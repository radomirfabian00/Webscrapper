import time
from typing import TextIO

import pandas as pd
import concurrent.futures
import re
import requests
import os
from bs4 import BeautifulSoup

from utils import *

CURRENT_DATE = get_current_date_hour()

# Auto assign pool of workers to maximum CPU cores.
# You can limit the amount by either inserting a manual number(MAX_WORKERS = 4)
# Or by dividing cpu_count ( MAX_WORKERS = os.cpu.count()/2 )
MAX_WORKERS = os.cpu_count()

# Header will serve as header parameter for requests
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}


@catch_errors
def logger(data, dir='raw') -> TextIO:
    """
    Logging will serve for tracking progress and training regex (manually)
    Could be used to fuel Machine Learning into recognizing addresses,
    As recognizing addresses is the greatest problem currently.
    :type return: Will return location of the file as str object
    """
    logs = get_logs_path(dir)
    file = get_filename(logs, CURRENT_DATE)
    with open(file, "a") as file:
        for address in data:
            file.write(f"{address}\n")
    file.close()
    print(f"Results have been saved to {file}")
    return file


@catch_errors
def grab_info(url) -> TextIO:
    """
    :param url: Input url (must contain https://)
    :type url: link
    :return: Returns the address value scrapped from the url
    :type return: string
    """

    def runtime_cleaner(addresses: list):
        cleaned_addresses = []
        pattern = r"[0-9]+ ([A-Za-z]+( [A-Za-z]+)+) [0-9]+"
        for address in addresses:
            address_without_commas = re.sub(",", "", address).strip()
            match = re.search(pattern, address_without_commas)  # Use regex to find the matched part of the address
            if match:
                cleaned_address = match.group(0).strip()
                cleaned_addresses.append(cleaned_address)
            else:
                pass
        return cleaned_addresses

    with requests.Session() as session:
        response = session.get(url, headers=HEADER, timeout=(2, 2))
        soup = BeautifulSoup(response.text, "html.parser")
        address_elements = soup.find_all(lambda tag: tag.name == 'p' and 'address' in tag.text.lower()) + \
                           soup.find_all('address') + \
                           soup.find_all(class_=['address', 'vcard', 'contact-text'])
        address = [element.get_text(separator=' ', strip=True) for element in address_elements]
        logger(address, 'raw')  # Log into dir raw
        address = runtime_cleaner(address)
        logger(address, 'data')
        return address


def process_row(row):
    url = "https://" + row['domain']
    address_info = grab_info(url)  # Replace grab_info with your actual function
    return address_info


def main():
    df = pd.read_parquet('websites.parquet')  # Read addresses from .parquet file
    # print(df) - Display the .parquet file

    # Uncomment this line to limit the sites that will be scrapped
    # df = df.head(200)

    # Parse the .parquet file using Pandas (Requires FastParser lib)
    # Now uses Multithreading for scrapping multiple websites in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_row, row) for _, row in df.iterrows()]
        concurrent.futures.wait(futures)


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    formatted_execution_time = "{:.2f}".format(execution_time)  # We only want with 2 decimals
    print(f"Execution time: {formatted_execution_time} seconds.")
