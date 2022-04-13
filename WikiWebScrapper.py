""" 
Web Scrapper to get pageviews data from Wikipedia's API per country
"""



from collections import deque
import requests
from bs4 import BeautifulSoup
import urllib3
import json


def main():
    apiList: deque = getUrls(2015, 2022)
    savePath = r'pageCountsByCountry/'
    for url in apiList:
        downloadData(url, savePath)
    
def downloadData(url, savePath):
    ''' 
    A method to download the data passed in from Wikipedia url and save it in its own json.
    '''
    try:
        http = urllib3.PoolManager()
        resp = http.request("GET", url)
        jsonContent: dict = json.loads(resp.data.decode('utf-8'))
        fileName = url.split('/')[-2] + '-' + url.split('/')[-1] 
        with open(savePath + fileName + ".json", 'w') as f:
            json.dump(jsonContent, f, indent=4)
    except: 
        # if there is an error write the date into a NA file.
        with open(r'pageCountsByCountry\\NAdates', 'a') as f:
            f.write(fileName + '\n')

def getUrls(startYear = 2016, endYear = 2021) -> deque: 
    ''' 
    A method that takes a startYear and an endYear(exclusive). It then
    returns a queue of all the URLs to scrap between these time
    intervals per month.  
    '''
    queue = deque()
    year: int = startYear
    month: int = 0
    while (year < endYear):
        month = 1 + (month % 12)
        stringMonth: str = str(month)
        stringYear: str = str(year)
        if month < 10:
            stringMonth = '0' + str(month)
        url = r'https://wikimedia.org/api/rest_v1/metrics/pageviews/top-by-country/en.wikipedia.org/all-access/{}/{}'.format(stringYear,stringMonth) 
        year = year + 1 if month %12 == 0 else year 
        queue.append(url)
    return queue
    
if __name__ == '__main__':
    main()