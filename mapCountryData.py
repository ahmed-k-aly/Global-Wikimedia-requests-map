""" 
This program filters the wikipedia API country's pageviews data.
It reads all the JSON files that have country data and exports 
them to a single CSV with the dates, the countries, and the data.
"""


import numpy as np
import os
import json
from datetime import datetime
import csv


def main():
    filesList = os.listdir('pageCountsByCountry')
    dataList: list = getDataList(filesList)
    dates, countries = getRowsCols(dataList)
    #write_to_csv(dates, countries, dataList)
    new_write_to_csv(dates, countries, dataList)


def new_write_to_csv(dates: list, countries: list, dataList: list):
    """ 
    This method exports the data in a CSV, but in a different format than
    the original write to csv method. The new format should be easier to
    handle with most of the plotting libraries. The format that the new
    CSV is in is Countries,Requests,Dates.
    """

    with open('newRequests_per_country.csv', 'w', newline='') as csvfile:
        fieldnames = ["Country", "Requests", "Dates"]
        theWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        theWriter.writeheader()
        for index in dataList:
            for key in index:
                if key == 'date':
                    continue
                theWriter.writerow(
                    {"Country": key, "Dates": index['date'], "Requests": index[key]})


def write_to_csv(dates: list, countries: list, dataList: list):
    """ 
    Exports the data to a CSV in the format of
            Country A,      CountryB,       etc...
    Date1,  numRequestsA,   numRequestsB,   etc...
    Date2,  numRequestsA,   numRequestsB,   etc...
    etc...
    """
    with open('requestsPerCountry.csv', 'w', newline='') as csvfile:
        fieldnames = ['date'] + countries
        theWriter = csv.DictWriter(
            csvfile, fieldnames=fieldnames, restval=np.nan)
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


def getDataList(jsonList) -> list:
    """ 
    Takes a list of all the files and returns a list of the number of
    requests, the country's name, and the date. The form the data 
    is arranged in is that every month is in an index of that list.
    The indices themselves are a dictionary with the 'first' entry as
    the date, and the rest are key: value pairs of country: requests.
    """

    allPagesList: list = []
    for file in jsonList:
        json_file = open('pageCountsByCountry/' + file, 'r')
        data: dict = json.load(json_file)
        json_file.close()
        oneJsonsDict: dict = getOneFilesData(data)
        allPagesList.append(oneJsonsDict)
    return allPagesList


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


def getOneCountriesData(countriesData: dict) -> dict:
    return {countriesData["country"]: countriesData["views_ceil"]}


if __name__ == '__main__':
    main()
