import os
from datetime import datetime
import concurrent.futures
import json


myDict: dict = dict()
dateList = []
def main():
    path: str = r'C:\Users\nitro\Downloads\Data\Extracted'
    filesList: list = os.listdir(path)
    with concurrent.futures.ThreadPoolExecutor() as executor:   
        executor.map(getData, filesList)
    with open("wikipedia.json", 'w') as f:
        json.dump(myDict, f, indent=4)


def myFunc(line: str) -> int:
    return int(line.split()[-2])


def getData(fileName: str):
    try:
        date: datetime = getTimeFromFileName(fileName)
        dateList.append(date)
        readData(fileName, date)
        print(fileName)
    except:
        with open("errors.log", 'w', newline='') as f:
            f.write(fileName)


def readData(fileName: str, date: datetime):
    """ 
    Reads the wikimedia data and gets the total traffic
    of every page by storing it in a dictionary with the
    page's name as the key with value another dictionary
    consisting of a time key and a number of requests at
    that time value {pageName: {time1: request1, time2: request2, etc}}.
    """
    path: str = r'C:\Users\nitro\Downloads\Data\Extracted\{}'.format(fileName)
    file = open(path, 'r', encoding="utf8")
    linesList: str = file.readlines()
    file.close()
    linesList.sort(reverse = True, key = myFunc)
    linesList: list = list(map(str.strip, linesList))
    for line in linesList[:50]:
        page: str = line.split()[0] + ',' + line.split()[1]
        traffic: int = int(line.split()[-2]) 
        if page in myDict: 
            """ If page was already trending,
            get the value back, modify it, 
            and put it back in the dictionary. 
            Else, just add the page to the dictionary.
            """
            value: dict = myDict[page]
            x = {date: traffic}
            value.update(x)
        else: 
            myDict[page] = {date:traffic}


def getTimeFromFileName(fileName: str):
    """
    Helper Method that takes filename and returns a dateTime object
    representing the time of the file name
    """
    
    filenameArr: list = fileName.split("-")
    dateTimeString = filenameArr[1] +"-" + filenameArr[-1][0:2]
    return dateTimeString


if __name__=='__main__':
    main()