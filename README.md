# Project In Progress
# Comparison of Energy Cost and Carbon Emissions for Air-Source Heat Pump and Natural Gas Furnaces in the US

# Abstract

Compared the energy costs and carbon emissions of air-source heat pumps (ASHPs) and natural gas furnaces in all US counties. Created a typical US single-family home model in the BEOpt (Building Energy Optimization) energy modeling software and exported two IDF files of the same house, with the only difference being one home using an ASHP, and the other using a natural gas furnace and air-conditioning unit. Using Python to perform bulk simulation in EnergyPlus, simulated the two idf files in all US counties using EPW weather files. Created data visualizations in Power BI and Python, which showed that ASHPs have lower emissions on the west coast and northeast US, and generally have lower operating costs in states with milder climates. 

# Method

01_extract_coordinates_from_epw.py

This file looped through all the epw files and extracted the following information about the weather station.

State
Name
Number
WMO
Latitude
Longitude

The ZIP Code of each weather station was also identified using the library Geopy. This attempt was unsuccesul in identifying all weather station ZIP codes. The original intent of determining weather station zip codes was to determine the subgrid associated with each county. Further along in the creation of this project, the FIPS number of each weather station was eventually determined to be located within the EPW file name.

The extracted information was saved to several files beginning with the name 'ZIP_CODES' and ending in a single digit. The final data was combined into the file ZIP_CODES_FINAL.csv.

02_station_to_fips.py

This file was used to extract the FIPS number from the weather station file name. I made this realization after starting this project, which would have eliminated the need to use Geopy in the python file, 01_extract_coordinates_from_epw.py. The extracted data was saved to the EPW_FIPS_ZIP_CODES.csv file.

03_assigning_subgrid_for_each_county.py

This file was used to assign a subgrid to each county.

Used a for loop to go through each county in the EPW_FIPS_ZIP_CODES.csv file. Using the FIPS number of a particular county, the ZIP codes of each county were isolated. This was done using the file ZIP-COUNTY_FIPS_2018-03.csv, which has all of the ZIP codes for each county. A datframe in Pandas was created for each county and all of its corresponding ZIP codes. Once the ZIP codes were determined, a subgrid was assigned to each ZIP code. This was done using the file ZIP_SUBREGION.csv, which is a file from the USEPA which has collected every ZIP Code in the US and its corresponding subgrid. Once a subgrid was assigned for all ZIP codes of a particular county, then the subgrids were tallied to determine which subgrid was represented the most frequently. For most counties, only a single subgrid exists, but for some counties that are split between two subgrids or even share two subgrids, this method was effective in assigning subgrids to each county. This information would later be used to determine the carbon emission for operating ASHPs in each county, based on the carbon emissions produced by a particular subgrid. 

![house_view](/images/house_iso_view.png)
 

![elec_prices](/images/state_maps_Page_1.jpg)
![np_prices](/images/state_maps_Page_2.jpg)
![elec_ng_ratio](/images/state_maps_Page_3.jpg)

![heatmap](/images/subgrid_map.png)

![heatmap](/images/heatmap_correlation.png)

![energy cost](/images/US_map_energy_cost.jpeg) 

![emissions](/images/US_map_emissions.jpeg)
