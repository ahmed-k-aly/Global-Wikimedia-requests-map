""" 
Program to plot the wikipedia page views data per country
as a Choropleth plot based on the intensity of the area
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import pycountry
import os
import pandas as pd
import plotly.offline as offline


def main():
    df, world = readData()
    df = cleanData(df, world)
    dataSlider = getAllDatesData(df)
    steps = getSliderSteps(dataSlider)
    sliders = [dict(active=0, pad={"t": 1}, steps=steps)]  
    layout = dict(geo=dict(scope='world',projection={'type': 'natural earth'}),sliders = sliders)
    fig = dict(data=dataSlider, layout=layout) 
    offline.plot(fig, auto_open=True,filename="enWikiRequestsPerCountry.html", validate=True)



def getSliderSteps(dataSlider):
    """ 
    Styles how the slider looks and adds text to the ticks
    """
    steps = []
    filesList = os.listdir('pageCountsByCountry')
    for i in range(len(dataSlider)):
        filesList[i] = filesList[i].replace('.json', '')
        step = dict(method='restyle',
                    args=['visible', [False] * len(dataSlider)],
                    label='Date {}'.format(filesList[i])) # label to be displayed for each step (year)
        step['args'][1][i] = True
        steps.append(step)
    return steps


def getAllDatesData(df):
    """ 
    Puts all the data for every date in a single list with every unique
    date in an index by itself 
    """
    dataSlider = []
    df['text'] = df['name'].map(str) + ': ' + df['Requests'].map(str) + ' Requests'
    scl = [[0.0,'#ffffcc'],[1.35E-6,'#ffeda0'],[5.415E-6,'#fed976'],[2.886E-5,'#feb24c'],[9.180E-4,'#fd8d3c'],
            [1.390E-2,'#fc4e2a'],[1.560E-1,'#e31a1c'],[1.0,'#800026']]
    
    for date in df.Dates.unique(): 
        if type(date) != str:
            continue
        date:str = date.replace("-01 00:00:00",'')
        new_df = chooseTimeInterval(df, date = date)
        new_df.dropna(inplace=True)
        data = getChoroplethData(new_df, scl)
        dataSlider.append(data)
    return dataSlider        
        
        
        

def getChoroplethData(df, scl) -> dict:
    """ 
    Gets data for a map from the passed dataFrame
    """
    data = dict(
            showscale = True,
            type='choropleth', # type of map-plot
            colorscale = scl,
            autocolorscale = False,
            locations = df['iso_a3'], # the column with the state
            z = df['Requests'].astype(float), # the variable I want to color-code
            locationmode = 'ISO-3',
            text = df['text'], # hover text
            marker = dict(     # for the lines separating states
                        line = dict (
                                color = 'black', 
                                width = 2) ),               
            colorbar = dict(
                        title = "enWiki Pageviews "),
            ) 
    return data

        
    



def checkForWrongDateInputs(date: str):
    """ 
    Helper Method that raises exception if an error is 
    caught relating to how the date was passed.
    """
    if type(date) != str:
        raise TypeError("Date type is {} instead of str".format(type(date)))
    elif len(date) != 7 or date[4] != '-':
        raise ValueError("Date is in the wrong format")
    splitDate = date.split('-')
    year = int(splitDate[0])
    month = int(splitDate[1])
    if year > 2021 or year < 2015:
        raise ValueError("Data only available from 2015 to 2021")
    elif year == 2015 and month < 5:
        raise ValueError("Data only available from 2015-05")
    elif year == 2021 and month >6:
        raise ValueError("Data only available until 2021-06")
    elif month > 12 or month < 1:
        raise ValueError("Months are only between 1 and 12")

def chooseTimeInterval(df, date: str) -> DataFrame:
    """ 
    Method that selects the data based on the date 
    argument that's passed. 
    Date to be entered as YYYY-MM
    """
    checkForWrongDateInputs(date)    
    date += '-01 00:00:00'
    toReturn = df.query("Dates == '{}' or Dates != Dates".format(date))
    toReturn = toReturn.reset_index(drop=True)
    return toReturn



def readData() -> DataFrame:    
    """ 
    Reads the csv data and the world data and returns them as a DataFrame
    """
    df = pd.read_csv('newRequests_Per_Country.csv')    
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    return df, world


def cleanData(df: DataFrame, world):
    """ 
    Merges the dataFrame with the world dataSet
    and cleans both dataFrames. 
    """
    changeCountryISOcode(df)
    removeBadCountries(df)
    world = world.merge(df, left_on='iso_a3', right_on='Country',how='left')
    world.drop(labels=['pop_est', 'continent', 'gdp_md_est', 'Country'],axis=1, inplace=True)
    world.reset_index(drop=True, inplace=True)
    return world


def plotData(df: DataFrame, date: str, color: str = 'YlOrRd'):
    """ 
    Plots the data in a map
    """
    df.plot(column='Requests',cmap = color,scheme = 'percentiles', figsize=(18,10), legend = True, edgecolor ='black', 
            missing_kwds={
        "color": "lightgrey",
        "edgecolor": "red",
        "hatch": "///",
        "label": "Missing values",
    })
    #removing axis ticks
    plt.axis('off')#Add the title
    plt.title("Number of the Wikipedia pageviews per country on " + date)
    plt.show()
    
def removeBadCountries(df):
    """ 
    Removes Countries with unknown ISO codes
    """
    df.query("Country != 'Unknown code'", inplace=True)
    df.reset_index(drop=True, inplace=True)    

def changeCountryISOcode(df):
    """ 
    Data was given with ISO code as iso2, had to change iso codes
    to iso3 to be able to merge data with the existing geometries 
    """
    input_countries = df["Country"].tolist()
    
    countries = {}
    for country in pycountry.countries:
        countries[country.alpha_2] = country.alpha_3
    codes = [countries.get(country, 'Unknown code') for country in input_countries]
    df["Country"] = codes
    
    
    
if __name__ == '__main__':
    main()