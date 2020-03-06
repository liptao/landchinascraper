import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time
import random
import os
from configparser import ConfigParser


parser = ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '..', 'config.cfg'))
cookie = parser.get('settings', 'cookie')
f = 'csvfile.csv'
outputLocation = os.path.join(os.path.dirname(__file__),
                              '..',
                              'output',
                              'data_raw_cn.xlsx')


class scraper:
    """
    Instance variables:
    cookie -- cookie of scraping session
    combinedData -- list of lists containing scraped data

    Methods:
    importData -- parses html text and appends to combinedData
    """

    def __init__(self):
        self._combinedData = []

    @property
    def combinedData(self):
        return self._combinedData

    def importData(self, html, url):
        """Appends html to instance"""
        # Get the soup
        soup = BeautifulSoup(html, 'html.parser')
        # Find the data table in the soup
        tab = soup.find(
            'table', id='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1')
        # Data columns
        cols = [
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c1_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c3_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r23_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl',
        ]
        # Get the data from the table
        data = []
        for i in cols:
            val = tab.find('span', id=i).text.strip()
            data.append(val)
        # Append URL
        data.append(url)
        self.combinedData.append(data)


def getURLs(f):
    """
    Get URLs from file list
    Input:
    f -- csv file name with links to transactions
    """
    path = os.path.join(os.path.dirname(__file__), '..', 'input', f)
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            yield row


def getHTML(url, cookie):
    """Get HTML text from urls"""
    # Wait in order to avoid IP ban
    x = random.randrange(3, 6)
    print('Waiting...', int(x), ' seconds')
    time.sleep(x)
    headers = {
        u'Accept': (u'text/html,application/xhtml+xml,application/xml;q=0.9,'
                    'image/webp,image/apng,*/*;q=0.8'),
        u'Accept-Encoding': u'gzip, deflate',
        u'Content-Type': u"application/x-www-form-urlencoded",
        u'Accept-Language': u'zh-CN,zh;q=0.9',
        u'User-Agent': (u'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                        'AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/71.0.3578.98 Safari/537.36'),
        u'Host': u'www.landchina.com',
        u'Cookie': cookie.encode('utf-8'),
        u'Cache-Control': u'max-age=0',
        u'Connection': u'keep-alive',
        u'Referer': (u'http://www.landchina.com/default.aspx?tabid=263&wmguid'
                     '=75c72564-ffd9-426a-954b-8ac2df0903b7&p=')
    }
    html = requests.get(url, headers=headers).text
    return (html, url)


def getDF(combinedData):
    '''
    Transforms list of lists to DF.
    Input:
    combinedData -- List of Lists
    Return:
    DataFrame
    '''
    print('Number of transactions: ', len(combinedData))
    colnames = ['District',
                'Electronic supervision number',
                'Project name',
                'Project location',
                'Area (hectare)',
                'Land source',
                'Land utilisation',
                'Land supply method',
                'Land use period in year',
                'Industry category',
                'Land grade',
                'Transaction price (ten thousand yuan)',
                'Installment payment agreement payment period number',
                'Installment payment agreement agreed payment date',
                ('Installment payment agreement agreed payment amount'
                 ' (ten thousand yuan)'),
                'Note',
                'Land use right holder Row 1',
                'Land use right holder Row 2',
                'Agreed floor area ratio lower limit',
                'Agreed floor area ratio upper limit',
                'Agreed land delivery time',
                'Agreed start time',
                'Agreed completion time',
                'Actual start time',
                'Actual completion time',
                'Authorised by',
                'Contract signing date',
                'URL'
                ]
    df = pd.DataFrame(combinedData, columns=colnames)
    print('DF shape: ', df.shape)
    return df


def exportData(df, outputLocation=outputLocation):
    """
    Exports DataFrame as Excel
    Inputs:
    df -- DataFrame to export
    outputLocation -- output location of excel, default is output folder
    """
    print('Exporting to ', outputLocation)
    df.to_excel(outputLocation, index=None,
                header=True, sheet_name='original data')
    print('Completed export to excel')


def main(f,
         cookie,
         outputLocation=outputLocation):
    i = 1
    # Initialize scraper instance
    s = scraper()
    # Loop through URLs
    for url in getURLs(f):
        print('URL #', i, ' ', url[0])
        # Get HTML text
        html, url = getHTML(url[0], cookie)
        # Append HTML data to scraper instance
        s.importData(html, url)
        i += 1
        print('Length of data: ', len(s.combinedData))
    # Get DataFrame
    df = getDF(s.combinedData)
    # Export DataFrame
    exportData(df, outputLocation)


if __name__ == "__main__":
    main(f, cookie)
