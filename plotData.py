""" 
Program to plot the wikipedia page views data per country
as a Choropleth plot based on the intensity of the area
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import pycountry
import contextily as ctx
import ipywidgets
import os
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)



def main():
    dateToLookAt = '2015-06'
    filesList = os.listdir('pageCountsByCountry')
    for date in filesList:
        df, world = readData()
        df = cleanData(df, world)

        date = date.replace('.json','')
        chooseTimeInterval(df, date = date)
        plotData(df, date)


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

def chooseTimeInterval(df, date: str):
    """ 
    Method that selects the data based on the date 
    argument that's passed. 
    Date to be entered as YYYY-MM
    """
    checkForWrongDateInputs(date)    
    date += '-01 00:00:00'
    df.query("Dates == '{}' or Dates != Dates".format(date), inplace=True)
    df.reset_index(drop=True, inplace=True)



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
    world.drop(labels=['pop_est', 'continent', 'gdp_md_est', 'Country',],axis=1, inplace=True)
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
    input_countries = df["Country"].tolist()
    
    countries = {}
    for country in pycountry.countries:
        countries[country.alpha_2] = country.alpha_3

    codes = [countries.get(country, 'Unknown code') for country in input_countries]
    df["Country"] = codes
    
    
    
if __name__ == '__main__':
    main()