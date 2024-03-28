# Webscrapper
Challenge project dedicated for webscraping using Python and BeautifulSoup library.
Pandas and FastParquet are strictly used for reading parquet file. Do not use them if you don't need to read a parquet.

If you receive import errors, run in terminal from the root of the project:
pip install -r requirements.txt

IMPORTANT: I will not provide the parquet file as it is not mine to share. Just get a list of websites or something to test it on.

## Current Objectives:

1. Use Python Multithreading for handling multiple connection requests.
   Reason: given a larger number of websites, it will take years to finish execution. (IMPLEMENTED)
2. Write info on the go, not with a middleman array. (IMPLEMENTED)
3. Code cleanup, removal of junk and all of that. (DONE)

## Problems
Catching addresses with pure code and regex will only get so many addresses.
The best way would be to use a paid API tool (generic example: https://www.webscrapingapi.com/)
  - I am not affiliated in any way with the site mentioned above, nor have I received any benefits. It is only an example of a scraping API

However, businesses don't like "paying monthly" and therefore, I found a far better solution.
This program here will output into the "raw" folder (subject of change) only addresses matching a certain regex (the standard US addresses)
 -These addresses could be fed into a Machine Learning, which later could decide if it is, or not, an address, which increases the chances of actually scrapping a real address substantially. Food for the thought.