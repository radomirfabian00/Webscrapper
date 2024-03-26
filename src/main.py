import pandas as pd
import requests
from bs4 import BeautifulSoup
import sys
import re

sys.path.append("C:/Users/Vanguard/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0/LocalCache/local-packages/Python312/site-packages")

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

def grab_info(url):
    try:
        with requests.Session() as session:
            response = session.get(url, headers=HEADER, timeout=(2,2))
            soup = BeautifulSoup(response.text, "html.parser")
            address_elements = soup.find_all(lambda tag: tag.name == 'p' and 'address' in tag.text.lower()) + \
                               soup.find_all('address') + \
                               soup.find_all(class_=['address','vcard','contact-text'])
            address = [element.get_text(separator=' ',strip=True) for element in address_elements]
            return address
    except Exception as error:
        print(f"Error: {error}")


def remove_prefix_from_addresses(addresses):
    def remove_prefix(address):
        # Define the regex pattern to match the prefix and the address part
        pattern = r"[\w\s]*:\s*(.*)"  # Match any prefix followed by zero or more whitespace characters

        # Use regex to find the matched part of the address
        match = re.search(pattern, address)

        if match:
            # Extract the matched part (group 1) and remove leading/trailing whitespace
            return match.group(1).strip()
        else:
            return address  # Return the original address if no match is found

    return [remove_prefix(address) for address in addresses]

def remove_non_addresses(addresses):
    pass
def main():
    addresses = []
    # Read addresses from .parquet file
    df = pd.read_parquet('websites.parquet')
    df = df.head(150)
    print(df)
    # Go through the .parquet file
    for _, row in df.iterrows():
        url = "https://" + row['domain']
        address_info = grab_info(url)
        if address_info:
            print("Address info extracted from", url)
            try:
                addresses.append(address_info.strip())
            except:
                addresses.append(address_info[0])

    addresses = remove_prefix_from_addresses(addresses)
    for address in addresses:
        print(address)

if __name__ == "__main__":
    main()