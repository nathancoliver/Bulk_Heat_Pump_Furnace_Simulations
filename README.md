# Comparison of Energy Cost and Carbon Emissions for Air-Source Heat Pump and Natural Gas Furnaces in the US

# Abstract

Compared the energy costs and carbon emissions of air-source heat pumps (ASHPs) and natural gas furnaces in all US counties. Created a typical US single-family home model in the BEOpt (Building Energy Optimization) energy modeling software and exported two IDF files of the same house, with the only difference being one home using an ASHP, and the other using a natural gas furnace and air-conditioning unit. Using Python to perform bulk simulation in EnergyPlus, simulated the two idf files in all US counties using EPW weather files. Created data visualizations in Power BI and Python, which showed that ASHPs have lower emissions on the west coast and northeast US, and generally have lower operating costs in states with milder climates. 

# Method

## Building Model - IDF File ##

The BEOpt energy modeling program was used to create the IDF building model file of a typical single-family home, as shown below. Two different scenarios, each with different heating and cooling systems, were modeled in BEOpt and exported as separate IDF files. The HVAC systems are summarized below.

* Scenario 1
  * Air-Source Heat Pump - SEER 22, 10 HSPF, Variable Speed 

* Scenario 2
  * AC Unit - SEER 22
  * Natural Gas Furnace - 95% AFUE

![house_view](/images/house_iso_view.png)

## Weather Files - EPW Files ##

The weather files were downloaded from the NREL website [1], which has TMY3 weather files for each US county. These weather files are used for the ComStock and ResStock software. There were missing weather files in certain US counties in Texas, Alaska, and Hawaii. Counties with missing weather files were replaced with EPW files of neighboring counties. Below is a list of the counties with the missing weather files

### List of Missing NREL TMY3 Weather Files ###

* 02100 - Haines, AK
* 02105 - Hoonah-Angoon, AK
* 02158 - Kusilvak, AK
* 02195 - Petersburg, AK
* 02198 - Prince of Wales-Hyder, AK
* 02230 - Skagway, AK
* 02275 - Wrangell, AK
* 02282 - Yakutat, AK
* 02290 - Yukon-Koyukuk, AK
* 15005 - Kalawao, HI
* 48151 - Fisher, TX
* 48263 - Kent, TX
* 48353 - Nolan, TX
* 48433 - Stonewall, TX

A request for clarification on the missing weather files was submitted on UnMet Hours, and the weather files have since been updated on the NREL website.

## US County Data Preparation ##

Certain information for each US county were needed prior to beginning the EnergyPlus simulations. The following information was collected, and the process is detailed in the summary for the following three Python files.

* County FIPS Number
* County Subgrid
* Weather Station Name

Other information was collected for each county, such as county name, and weather station latitude and longitude, but the above three sets of information were vital in performing the energy and carbon emission calculations.

### Summary of Python Files Used for US County Information Data Preparation ###

#### 01_extract_coordinates_from_epw.py ####

This file looped through all the epw files and extracted the following information about each weather station.

* State
* Name
* Number
* WMO
* Latitude
* Longitude

The ZIP Code of each weather station was also identified using the library Geopy. This attempt was unsuccesul in identifying all weather station ZIP codes. The original intent of determining weather station zip codes was to determine the subgrid associated with each county. Further along in the creation of this project, the FIPS number of each weather station was eventually determined to be located within the EPW file name.

The extracted information was saved to several files beginning with the name 'ZIP_CODES' and ending in a single digit. The final data was combined into the file ZIP_CODES_FINAL.csv.

#### 02_station_to_fips.py #### 

This file was used to extract the FIPS number from the weather station file name. I made this realization after starting this project, which would have eliminated the need to use Geopy in the python file, 01_extract_coordinates_from_epw.py. The extracted data was saved to the EPW_FIPS_ZIP_CODES.csv file.

#### 03_assigning_subgrid_for_each_county.py #### 

This file was used to assign a subgrid to each county.

Used a for loop to go through each county in the EPW_FIPS_ZIP_CODES.csv file. Using the FIPS number of a particular county, the ZIP codes of each county were isolated. This was done using the file ZIP-COUNTY_FIPS_2018-03.csv, which has all of the ZIP codes for each county. A datframe in Pandas was created for each county and all of its corresponding ZIP codes. Once the ZIP codes were determined, a subgrid was assigned to each ZIP code. This was done using the file ZIP_SUBREGION.csv, which is a file from the USEPA which has collected every ZIP Code in the US and its corresponding subgrid. Once a subgrid was assigned for all ZIP codes of a particular county, then the subgrids were tallied to determine which subgrid was represented the most frequently. For most counties, only a single subgrid exists, but for some counties that are split between two subgrids or even share two subgrids, this method was effective in assigning subgrids to each county. This information would later be used to determine the carbon emission for operating ASHPs in each county, based on the carbon emissions produced by a particular subgrid. 

## County-Based Map of Electrical Grid Subregion ##

The map shown below on the left is the grid subregion map created by the US EPA. Each region of the grid has a different mix of fuels, with some using more energy from renewable sources, such as wind and solar, whereas other regions use more fossil fuels. The data collected in the 03_assigning_subgrid_for_each_county.py helped to create a map showing the different grid subregions at the county level, which when compared to the US EPA created map, shows a close match.
![grid_subregion_map](/images/grid_subregion_map_comparison.JPG)

## Electricity and Natural Gas Prices ##

State-level electricity and natural gas residential prices were used to calculate the energy costs of operating ASHPs, air conditioning units and natural gas furnaces. The electricity and natural gas residential prices for each state were collected from the USEIA website. County-level prices were not readily available, so state-level prices were used instead.

### US State Electricity Prices ###
![elec_prices](/images/state_maps_Page_1.jpg)
### US State Natural Gas Prices ###
![np_prices](/images/state_maps_Page_2.jpg)
### Comparison of Electricity and Natural Gas Prices ###

The ratio of electricity to natural gas prices provides a good indicator of the relative costs of operating ASHPs and natural gas furnaces. The units for both sets of prices are different, since electricity uses ¢/kWh, and natural gas uses USD/MCF. The key here is converting the volume of natural gas, which is in MCF (millions of cubic feet) to units of energy. The average heat content for natural gas in the US in 2021 was 1037 BTU/CF [2] Below shows the calculations used to convert the prices of natural gas and electricity into the USD/MMBtu.
![ng_elec_price_conversion](/images/ng_elec_price_conversion.png) 
![elec_ng_ratio](/images/state_maps_Page_3.jpg)

## Bulk EnergyPlus Simulations  ##

A simulation for each of the two building IDF files were simulated with each weather file using a Python script. It was discovered during the project that most of the weather files have duplicates, due to the fact that not all counties have available weather data. Every county has its own EPW weather file, but the same weather station's data could be used for multiple counties, meaning that if not performed correctly, the same weather file could essentially be unnecessarily simulated multiple times.  In order to save time performing simulations, once a weather station was simulated, the weather station's name was added to an array in Python. While inside the bulk simulation's FOR loop, if the script has already simulated weather station, then the simulation for that county is skipped and instead copies the already simulated energy data for that weather station. This ensured a weather station's EPW file was only used once, and reduced simulation time by approximately 75%.  For each simulation, the necessary data was extracted from html files that were exported from the EnergyPlus simulations and saved into a csv file.

## Calculating Energy Costs and Carbon Emissions ##

![elec_ng_cost_emissions](/images/ng_elec_price_emissions_calculations.png)

# Results #

## Energy Cost Comparison of Air-Source Heat Pumps and Natural Gas Furnace/Air Conditioner Combination ## 

![energy cost](/images/US_map_energy_cost.jpeg)
<!-- ![energy cost](/images/county_maps_Page_1.jpg) -->





## Carbon Emission Comparison of Air-Source Heat Pumps and Natural Gas Furnace/Air Conditioner Combination ## 

![emissions](/images/US_map_emissions.jpeg)
<!-- ![energy cost](/images/county_maps_Page_2.jpg) -->

![heatmap](/images/heatmap_correlation.png)



References

[1] https://data.nrel.gov/submissions/156
[2] https://www.eia.gov/dnav/ng/ng_cons_heat_a_EPG0_VGTH_btucf_a.htm
