""" 
Program to plot the wikipedia page views data per country
as a Choropleth plot based on the intensity of the area
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pycountry
import contextily as ctx

def main():
    df = pd.read_csv('newRequests_Per_Country.csv')    
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    changeCountryISOcode(df)
    removeBadCountries(df)
    world = world.merge(df, left_on='iso_a3', right_on='Country',how='left')
    world.drop(labels=['pop_est', 'continent', 'gdp_md_est', 'Country',],axis=1, inplace=True)
    world.query("Dates == '2015-05-01 00:00:00' or Dates != Dates", inplace=True)
    world.reset_index(drop=True, inplace=True)

    world.plot(column='Requests',cmap='YlOrRd',scheme = 'percentiles', figsize=(18,10), legend = True, edgecolor ='black', 
            missing_kwds={
        "color": "lightgrey",
        "edgecolor": "red",
        "hatch": "///",
        "label": "Missing values",
    })
    

    #removing axis ticks
    plt.axis('off')#Add the title
    plt.title("Number of the Wikipedia pageviews per country")
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