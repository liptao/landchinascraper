# landchinascraper

Scrapes land transaction results data (结果公告) from https://www.landchina.com.

## Features

- Uses request, BeautifulSoup, and pandas
 
- Able to output analysis ready DataFrame and Excel spreadsheet

- Relatively lightweight

## Instructions 

Running `python landchinascraper.py` scrapes links located in `input/csvfile.csv` and will output an Excel file in `output`. The current `output` folder contains an example output file.
Before running the package/script, a cookie needs to be inputted in the `config.cfg` file. The cookie can be retreived using developer tools on any transaction link from landchina and looks something like this:
```
ASP.NET_SessionId=uzxbjshvgeh4g2xl3xahpou5; security_session_verify=9364fe2c49ef5222db06c2779cadefa0; security_session_mid_verify=6156920c45117f09ba99d9cf560f6f7f
```
Be aware that the scraper includes random pauses to prevent detection and IP blocks from the website. The pauses may be shortened, but I kept them to 3-6 seconds to be safe.
## TODO

- Add a selenuim scraper to get links from landchina based on date and location filters.
- Add feature to automatically get cookie.
