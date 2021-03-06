# Global-Wikimedia-requests-map
> A project visualising global requests to all the English articles under Wikimedia over a time interval.
## Data Gathering:
> Data was gathered through wikimedia's REST API https://wikimedia.org/api/rest_v1/.
> We collected data from may 2015 until may 2021.
## Implementation:
> First, the data was collected in seperate json files with each file representing a month worth of requests for each country.
> Next, a script was written to convert the data into one csv file where each country is associated with all of its data.
> To plot the data, we used geopandas's GIS system. Thus, we needed to use the ISO Alpha 3 Numeric Code to be able to map each country to its geographical spot on the map. Therefore, we needed to clean the data and run an algorithm that converts each countries to their respective ISO-3 codes while handling the edge cases of countries that were not recognized.
> Lastly, we used plotly to create the map and design it
## Chropleth map
## Key Features:
> The map is very interactive and labeled where by hovering over each country, you get to see its current requests and the log of that for the month you chose.
> 
> The map utilizes a slider that changes the current year of interest.
>
> It is also possible to highlight and zoom into different parts of the world for a focused perspective.
## Images:
### May 2015 snapshot
### ![May-2015](https://github.com/ahmed-k-aly/Global-Wikimedia-requests-map/blob/7be252600c6498e61ba9591c8426d370e486de6f/2015-05%20Map.png)
### July 2020 snapshot
### ![July-2020](https://github.com/ahmed-k-aly/Global-Wikimedia-requests-map/blob/7be252600c6498e61ba9591c8426d370e486de6f/2020-07%20Map.png)
### South America and Africa focus
### ![Highlighting](https://github.com/ahmed-k-aly/Global-Wikimedia-requests-map/blob/580b4fc7171942245c6f223a913d3194fcaa30cf/Highlighting.png)

