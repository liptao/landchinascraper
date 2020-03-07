# landchinascraper

Scrapes land transaction results data (结果公告) from https://www.landchina.com.

## Features

- linkscraper.py - finds transaction result links based on date range and county and outputs links in csv
  - Requires selenium(ChromeDriver) and BeautifulSoup
  - ChromeDriver download here (confirm your version): https://chromedriver.chromium.org/
- landchinascraper.py - scrapes transaction result links from csv 
  - Requires requests, BeautifulSoup, and Pandas
  - Able to output analysis ready DataFrame and Excel spreadsheet

## Instructions 

If `linkscraper.py` or `landscraper.py` are run directly, please edit the `config.cfg` file first. 

### linkscraper

Running `linkscraper.py`  directly requires the following parameters in `config.cfg`:

- driverLocation: path to ChromeDriver
- startDate: start date of search in yyyy-m-d
- endDate: end date of search yyyy-m-d
- county: county location
- countyKey: the county key used by landchina.com. To find code, submit a query with your county of interest and check the source code for the value attribute for `id="TAB_queryTblEnumItem_256_v"`

The current `config.cfg` file contains an example search for Beijing (北京市本级) , date range from 2019-1-1 to 2019-6-30, and the county key is 110100.

`python linkscraper.py` will directly output a csv of URLs to`input/URLs.csv`.

`linkscraper.py`can also be imported. Example of usage:

```python
# Step 1
# Initialize driver instance
# Specify headless=True if you want to run a headless browser, default is False
driver = driver(chromedriverPath='/path/to/chromedriver.exe',
                startDate='2019-1-1',
                endDate='2019-6-30',
                county='北京市本级',
                countyKey='110100',
                headless=True)
# Step 2
# Conduct search with parameters specified
driver.search()

# Step 3
# Scrape all links of every page found under search
driver.scrapeLinks()

# Step 4
# Export CSV file to outputlocation
# Running linkscraper.py will default to exporting to input\URLs.csv
driver.getCSV(outputlocation)
```

### landchinascraper

Running `python landchinascraper.py` scrapes links located in `input/URLs.csv` and will output a file to `output/data_raw_cn.xlsx`. The current `output` folder contains an example output file named `data_raw_cn.xlsx`.

Be aware that the scraper includes random pauses to prevent detection and IP blocks from the website. The pauses are 1-4 seconds to be safe, but you might be able to get away with shorter pauses.

For the scraper to work, you must edit the cookie needs to be inputted in the `config.cfg` file. The cookie can be retrieved using developer tools on any transaction link from landchina and looks something like this:
![cookie](images/cookie.png).
The format of the cookie to paste will look something like this:

```
ASP.NET_SessionId=uzxbjshvgeh4g2xl3xahpou5; security_session_verify=9364fe2c49ef5222db06c2779cadefa0; security_session_mid_verify=6156920c45117f09ba99d9cf560f6f7f
```

`landchinascraper.py` can also be directly imported. Example of usage:

```python
# Step 1
# Initialize scraper instance
s = scraper()
# Loop through URLs using getURLs function
# f is location of URLs.csv
for url in getURLs(f):
	# Get HTML text from URL
	html, url = getHTML(url[0], cookie)
	# Scrape HTML data and and store the data and url to scraper instance
	s.importData(html, url)
# Get DataFrame from scraper instance
# scraper instance stores data as list of lists which can be accessed through s.combinedData
df = getDF(s.combinedData)
# Export DataFrame as .xlsx file to outputlocation
exportData(df, outputLocation)
```