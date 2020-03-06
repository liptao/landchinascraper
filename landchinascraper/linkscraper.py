from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re


class driver:
    """
    Driver instance
    """

    def __init__(self, chromedriverPath,
                 startDate='',
                 endDate='',
                 county='',
                 countyKey='',
                 headless=False):
        """
        Initialize driver instance
        """
        self._default = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default'
        self.startDate = startDate
        self.endDate = endDate
        self.county = county
        self.countyKey = countyKey
        options = Options()
        if headless:
            options.headless = True
        self._driver = webdriver.Chrome(chromedriverPath, options=options)
        self._URLList = []

    def _goToLocation(self):
        self._driver.get(self._default)

    def _enterSearchParams(self):
        # Enter parameters
        WebDriverWait(self._driver, 20).until(
            EC.element_to_be_clickable(
                (By.ID, 'TAB_QueryConditionItem270')
            )
        ).click()
        self._driver.find_element_by_id('TAB_queryDateItem_270_1').clear()
        self._driver.find_element_by_id(
            'TAB_queryDateItem_270_1').send_keys(self.startDate)
        self._driver.find_element_by_id('TAB_queryDateItem_270_2').clear()
        self._driver.find_element_by_id(
            'TAB_queryDateItem_270_2').send_keys(self.endDate)
        self._driver.find_element_by_id('TAB_queryTblEnumItem_256').clear()
        self._driver.find_element_by_id(
            'TAB_queryTblEnumItem_256').send_keys(self.county)
        self._driver.find_element_by_id('TAB_QueryConditionItem256').click()
        self._driver.execute_script(
            "document.getElementById('TAB_queryTblEnumItem_256_v').setAttribute('type', 'text');")
        self._driver.find_element_by_id('TAB_queryTblEnumItem_256_v').clear()
        self._driver.find_element_by_id(
            'TAB_queryTblEnumItem_256_v').send_keys(self.countyKey)
        self._driver.find_element_by_id('TAB_QueryButtonControl').click()

    def _getPages(self):
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

    def cyclePages(self):
        """Recursive function to cycle through pages"""
        currentPage, totalPages, pageSelector = self._getPages()
        print('On page ', currentPage, ' of ', totalPages, 'total pages')
        self._getLinksFromTable()
        if currentPage < totalPages:
            pageSelector[0].clear()
            pageSelector[0].send_keys(currentPage + 1)
            pageSelector[1].click()
            self.cyclePages()
        else:
            print('Done!')

    def quitDriver(self):
        self._driver.quit()


driver = driver('C:/Users/etao/Developer/chromedriver/chromedriver.exe',
                startDate='2010-1-1', endDate='2020-3-6', county='靖边县', countyKey='610824')
driver._goToLocation()
driver._enterSearchParams()
driver.cyclePages()
driver.quitDriver()
