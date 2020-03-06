# landchinascraper

Scrapes land transaction results data (结果公告) from https://www.landchina.com.

## Features

- Uses request, BeautifulSoup, and pandas
 
- Able to output analysis ready DataFrame and Excel spreadsheet

## Instructions 

Running `python landchinascraper.py` scrapes links located in `input/csvfile.csv` and will output an Excel file in `output`. The current `output` folder contains an example output file.
## TODO

Add a selenuim scraper to get links from landchina based on data and location filters.
