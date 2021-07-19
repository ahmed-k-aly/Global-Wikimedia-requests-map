import os
import json
from datetime import datetime
import csv

def main():
    filesList = os.listdir('pageCountsByCountry')
    dataList: list = getDataDict(filesList)
    dates, countries = getRowsCols(dataList)
    write_to_csv(dates, countries, dataList)
    
    
    
def write_to_csv(dates: list, countries: list, dataList: list):
    with open('requestsPerCountry.csv', 'w', newline='') as csvfile:
        fieldnames = ['date'] + countries
        theWriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
        theWriter.writeheader()
        for index in dataList:
            theWriter.writerow(index)                
                

def getRowsCols(dataList: list) -> list:
    dateList = []
    countryList = []
    for index in dataList:
        dateList.append(index['date'])
        for key in index:
            if key == 'date':
                continue
            if key not in countryList:
                countryList.append(key)
    return dateList, countryList

def getDataDict(jsonList) -> list:
    allPagesDict: list = []
    for file in jsonList:
        json_file = open('pageCountsByCountry/' +file, 'r')
        data: dict = json.load(json_file)
        json_file.close()
        oneJsonsDict: dict = getOneFilesData(data)
        allPagesDict.append(oneJsonsDict)
    return allPagesDict    

def getOneFilesData(json: dict) -> dict:
    """ 
    Method that handles one Json file and returns a dict
    with all of its countries and the pageviews
    """
    pageDict: dict = {}
    json: dict = json['items'][0]
    date: str = json['year'] + '-' + json['month']
    date: datetime = datetime.strptime(date, '%Y-%m')
    pageDict['date'] = date
    countriesList: list = json['countries']
    for country in countriesList:
        oneCountriesData: dict = getOneCountriesData(country)
        pageDict.update(oneCountriesData)
    return pageDict


def getOneCountriesData(countriesData: dict)-> dict:    
    return {countriesData["country"] : countriesData["views_ceil"]}


if __name__ == '__main__':
    main()