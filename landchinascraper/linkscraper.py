from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import os
import csv
from configparser import ConfigParser

parser = ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__),
                         '..', 'config.cfg'), encoding='utf-8')
driverLocation = parser.get('linkscraper settings', 'driverLocation')
startDate = parser.get('linkscraper settings', 'startDate')
endDate = parser.get('linkscraper settings', 'endDate')
county = parser.get('linkscraper settings', 'county')
countyKey = parser.get('linkscraper settings', 'countyKey')

outputLocation = os.path.join(os.path.dirname(__file__),
                              '..',
                              'input',
                              'URLs.csv')


class driver:
    """Driver instance"""

    def __init__(self, chromedriverPath,
                 startDate='',
                 endDate='',
                 county='',
                 countyKey='',
                 headless=False):
        """
        Initialize driver instance
        """
        self._default = (
            'http://www.landchina.com/default.aspx?tabid=263&ComName=default'
        )
        self._startDate = startDate
        self._endDate = endDate
        self._county = county
        self._countyKey = countyKey
        options = Options()
        if headless:
            options.headless = True
        self._driver = webdriver.Chrome(chromedriverPath, options=options)
        self._URLList = []

    # Getters and Setters
    @property
    def startDate(self):
        return self._startDate

    @startDate.setter
    def startDate(self, newStartDate):
        self._startDate = newStartDate

    @property
    def endDate(self):
        return self._endDate

    @endDate.setter
    def endDate(self, newEndDate):
        self._endDate = newEndDate

    @property
    def county(self):
        return self._county

    @county.setter
    def county(self, newCounty):
        self._county = newCounty

    @property
    def countyKey(self):
        return self._countyKey

    @countyKey.setter
    def countyKey(self, newCountyKey):
        self._countyKey = newCountyKey

    @property
    def URLList(self):
        return self._URLList

    @URLList.setter
    def URLList(self, newURLList):
        self._URLList = newURLList

    def _goToLocation(self):
        self._driver.get(self._default)

    def _enterSearchParams(self):
        """Enter search filter parameters"""
        # Enter parameters
        WebDriverWait(self._driver, 20).until(
            EC.element_to_be_clickable(
                (By.ID, 'TAB_QueryConditionItem270')
            )
        ).click()
        self._driver.find_element_by_id('TAB_queryDateItem_270_1').clear()
        self._driver.find_element_by_id(
            'TAB_queryDateItem_270_1').send_keys(self._startDate)
        self._driver.find_element_by_id('TAB_queryDateItem_270_2').clear()
        self._driver.find_element_by_id(
            'TAB_queryDateItem_270_2').send_keys(self._endDate)
        self._driver.find_element_by_id('TAB_queryTblEnumItem_256').clear()
        self._driver.find_element_by_id(
            'TAB_queryTblEnumItem_256').send_keys(self._county)
        self._driver.find_element_by_id('TAB_QueryConditionItem256').click()
        self._driver.execute_script(
            ("document.getElementById('TAB_queryTblEnumItem_256_v')"
             ".setAttribute('type', 'text');")
        )
        self._driver.find_element_by_id('TAB_queryTblEnumItem_256_v').clear()
        self._driver.find_element_by_id(
            'TAB_queryTblEnumItem_256_v').send_keys(self._countyKey)
        self._driver.find_element_by_id('TAB_QueryButtonControl').click()

    def search(self):
        self._goToLocation()
        self._enterSearchParams()

    def _getPages(self):
        """Get current page and total pages"""
        p = self._driver.find_elements_by_css_selector('.pager')
        # If list is not empty
        if p:
            text = p[1].text
            reg = re.findall(r'\d+', text)
            totalPages = int(reg[0])
            pageSelector = self._driver.find_elements_by_css_selector(
                ".pager>input")
            currentPage = int(pageSelector[0].get_attribute('value'))
        # If list is empty there is only one page
        else:
            totalPages = 1
            currentPage = 1
            pageSelector = None
        return currentPage, totalPages, pageSelector

    def _getLinksFromTable(self):
        html = self._driver.find_element_by_id(
            'TAB_contentTable').get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        href = soup.select('.queryCellBordy a')
        for line in href:
            url = 'http://www.landchina.com/' + line['href']
            self._URLList.append(url)
            print('Added URL: ', url, '. Total urls')

    def scrapeLinks(self):
        """Recursive function to cycle through pages"""
        currentPage, totalPages, pageSelector = self._getPages()
        print('On page ', currentPage, ' of ', totalPages, 'total pages')
        self._getLinksFromTable()
        if currentPage < totalPages:
            pageSelector[0].clear()
            pageSelector[0].send_keys(currentPage + 1)
            pageSelector[1].click()
            self.scrapeLinks()
        else:
            print('Done!')

    def getCSV(self, outputLocation):
        """Export CSV file with links from URLList"""
        with open(outputLocation, 'w', newline='') as csvResults:
            writer = csv.writer(csvResults, dialect='excel')
            for u in self._URLList:
                writer.writerow([u])
        print('Exported CSV to ', outputLocation)

    def quitDriver(self):
        """Quit selenium driver"""
        self._driver.quit()


if __name__ == "__main__":
    driver = driver(chromedriverPath=driverLocation,
                    startDate=startDate,
                    endDate=endDate,
                    county=county,
                    countyKey=countyKey,
                    headless=True)
    driver.search()
    driver.scrapeLinks()
    driver.getCSV(outputLocation)
    driver.quitDriver()
