import eppy
import pandas as pd
import sys
from eppy import modeleditor
from eppy.modeleditor import IDF
from eppy.results import readhtml
import pprint
import csv

def read_file(path):
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    return df

path = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/new_file.csv'

temp = 'TEMP3'

df = read_file(path)

# df = df[df['FIPS'] > 00000]
# df = df[df['FIPS'] < 56000]

column = ['el_src_h1',
'el_sit_h1',
'el_sit_sub_h1',
'el_del_h1',

'el_src_c1',
'el_sit_c1',
'el_sit_sub_c1',
'el_del_c1',

'ng_src_h1',
'ng_sit_h1',
'ng_del_h1',

'ng_src_c1',
'ng_sit_c1',
'ng_del_c1',

'el_src_h2',
'el_sit_h2',
'el_sit_sub_h2',
'el_del_h2',

'el_src_c2',
'el_sit_c2',
'el_sit_sub_c2',
'el_del_c2',

'ng_src_h2',
'ng_sit_h2',
'ng_del_h2',

'ng_src_c2',
'ng_sit_c2',
'ng_del_c2',

'el_sit_t1',
'ng_sit_t1',
'el_sit_t2',
'ng_sit_t2']

for col in column:
    df[col] = ''

df = df.reset_index()

print(df)

station_sim = []

for n in range(len(df)):
    weather_file = df.loc[n,'Station_Number']
    station_name = df.loc[n,'Station_Name']

    if station_name in station_sim:
        print('*** STATION SKIPPED ***')
        index = df.index[df['Station_Name'] == station_name]
        copy = index[0]


        print('first station name ', copy, '  ', df.loc[copy,'Station_Name'])
        print('second station name', n, '  ', df.loc[n,'Station_Name'])

        for col in column:

            df.loc[n,col] = df.loc[copy,col]
            print(col, ' ', n, ' ', copy)
            print('original', df.loc[copy,col])
            print('new     ', df.loc[n,col])
            print('')

        continue

    else:
        print('*** STATION NOT SKIPPED ***')
        station_sim.append(station_name)

# idd file defines the E+ program
# epw is the weather file




# # define E+ version

    idd_file = 'C:/EnergyPlusV8-8-0/Energy+.idd'

# # define weather epw file

    epw_file = 'C:/Users/nathan.oliver/Documents/BEopt_2.8.0/' + temp + '/' + str(weather_file) + '.epw'

# # idf file contains all the information about the building

    idf_file_1 = 'C:/Users/nathan.oliver/Documents/BEopt_2.8.0/' + temp + '/1.idf'
    idf_file_2 = 'C:/Users/nathan.oliver/Documents/BEopt_2.8.0/' + temp + '/2.idf'


# # output file defines where the data will be saved
    output_file_1 = 'C:/Users/nathan.oliver/Documents/BEopt_2.8.0/' + temp + '/output1'
    output_file_2 = 'C:/Users/nathan.oliver/Documents/BEopt_2.8.0/' + temp + '/output2'


# # setiddname calls the E+ version to be used for the simulation
    IDF.setiddname(idd_file)


# #IDF defines which idf and epw files will be used for the simulation
    idf_1 = IDF(idf_file_1, epw_file)
    idf_2 = IDF(idf_file_2, epw_file)





    idf_1.printidf()
    idf_2.printidf()

    results_1 = idf_1.run(output_directory=output_file_1)
    results_2 = idf_2.run(output_directory=output_file_2)


#  # the eppy module with functions to read the html
    html_1 = 'C:/Users/nathan.oliver/Documents/BEopt_2.8.0/' + temp + '/output1/eplustbl.htm'
    html_2 = 'C:/Users/nathan.oliver/Documents/BEopt_2.8.0/' + temp + '/output2/eplustbl.htm'
    open_html_1 = open(html_1, 'r').read()
    open_html_2 = open(html_2, 'r').read()

# # titletable function reads data in html file
    tbl_1 = readhtml.titletable(open_html_1)
    tbl_2 = readhtml.titletable(open_html_2)

    source_1 = tbl_1[19][1]
    site_1 = tbl_1[3][1]
    site_1_sub = tbl_1[4][1]
    delivered_1 = tbl_1[62][1]

    source_2 = tbl_2[19][1]
    site_2 = tbl_2[3][1]
    site_2_sub = tbl_2[4][1]
    delivered_2 = tbl_2[62][1]

# h1 and c1 are heating and cooling for point 1 (Heat Pump)
# h2 and c2 are heating and cooling for point 2 (AC unit and NG Furnace)
# custom crankcase heater

    el_src_h1 = source_1[1][1]
    el_sit_h1 = site_1[1][1]
    el_sit_sub_h1 = site_1_sub[9][2] + site_1_sub[12][2]/2
    el_del_h1 = delivered_1[19][1]

    df.loc[n,'el_src_h1'] = el_src_h1
    df.loc[n,'el_sit_h1'] = el_sit_h1
    df.loc[n,'el_sit_sub_h1'] = el_sit_sub_h1
    df.loc[n,'el_del_h1'] = el_del_h1

    el_src_c1 = source_1[2][1]
    el_sit_c1 = site_1[2][1]
    el_sit_sub_c1 = site_1_sub[12][2]/2
    el_del_c1 = delivered_1[18][1]

    df.loc[n,'el_src_c1'] = el_src_c1
    df.loc[n,'el_sit_c1'] = el_sit_c1
    df.loc[n,'el_sit_sub_c1'] = el_sit_sub_c1
    df.loc[n,'el_del_c1'] = el_del_c1

    ng_src_h1 = source_1[1][2]
    ng_sit_h1 = site_1[1][2]
    ng_del_h1 = 0

    df.loc[n,'ng_src_h1'] = ng_src_h1
    df.loc[n,'ng_sit_h1'] = ng_sit_h1
    df.loc[n,'ng_del_h1'] = ng_del_h1

    ng_src_c1 = source_1[2][2]
    ng_sit_c1 = site_1[2][2]
    ng_del_c1 = 0

    df.loc[n,'ng_src_c1'] = ng_src_c1
    df.loc[n,'ng_sit_c1'] = ng_sit_c1
    df.loc[n,'ng_del_c1'] = ng_del_c1

    el_src_h2 = source_2[1][1]
    el_sit_h2 = site_2[1][1]
    el_sit_sub_h2 = site_2_sub[9][2] + site_2_sub[12][2]/2
    el_del_h2 = 0

    df.loc[n,'el_src_h2'] = el_src_h2
    df.loc[n,'el_sit_h2'] = el_sit_h2
    df.loc[n,'el_sit_sub_h2'] = el_sit_sub_h2
    df.loc[n,'el_del_h2'] = el_del_h2

    el_src_c2 = source_2[2][1]
    el_sit_c2 = site_2[2][1]
    el_sit_sub_c2 = site_2_sub[12][2]/2
    el_del_c2 = delivered_2[18][1]

    df.loc[n,'el_src_c2'] = el_src_c2
    df.loc[n,'el_sit_c2'] = el_sit_c2
    df.loc[n,'el_sit_sub_c2'] = el_sit_sub_c2
    df.loc[n,'el_del_c2'] = el_del_c2

    ng_src_h2 = source_2[1][2]
    ng_sit_h2 = site_2[1][2]
    ng_del_h2 = delivered_2[19][1]

    df.loc[n,'ng_src_h2'] = ng_src_h2
    df.loc[n,'ng_sit_h2'] = ng_sit_h2
    df.loc[n,'ng_del_h2'] = ng_del_h2

    ng_src_c2 = source_2[2][2]
    ng_sit_c2 = site_2[2][2]
    ng_del_c2 = 0

    df.loc[n,'ng_src_c2'] = ng_src_c2
    df.loc[n,'ng_sit_c2'] = ng_sit_c2
    df.loc[n,'ng_del_c2'] = ng_del_c2

    el_sit_t1 = site_1[16][1]
    ng_sit_t1 = site_1[16][2]
    el_sit_t2 = site_2[16][1]
    ng_sit_t2 = site_2[16][2]

    df.loc[n,'el_sit_t1'] = el_sit_t1
    df.loc[n,'ng_sit_t1'] = ng_sit_t1
    df.loc[n,'el_sit_t2'] = el_sit_t2
    df.loc[n,'ng_sit_t2'] = ng_sit_t2



    print('Electrcity','Natural_Gas')
    print('HP','Heating','Source',el_src_h1,ng_src_h1)
    print('HP','Heating','Site',el_sit_h1,ng_sit_h1)
    print('HP','Heating','Delivered',el_del_h1,ng_del_h1)
    print('HP','Cooling','Source',el_src_c1,ng_src_c1)
    print('HP','Cooling','Site',el_sit_c1,ng_sit_c1)
    print('HP','Cooling','Delivered',el_del_c1,ng_del_c1)
    print('NG_AC','Heating','Source',el_src_h2,ng_src_h2)
    print('NG_AC','Heating','Site',el_sit_h2,ng_sit_h2)
    print('NG_AC','Heating','Delivered',el_del_h2,ng_del_h2)
    print('NG_AC','Cooling','Source',el_src_c2,ng_src_c2)
    print('NG_AC','Cooling','Site',el_sit_c2,ng_sit_c2)
    print('NG_AC','Cooling','Delivered',el_del_c2,ng_del_c2)
    print('HP','Total','Site',el_sit_t1,ng_sit_t1)
    print('NG_AC','Total','Site',el_sit_t2,ng_sit_t2)



    path = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/bulk_simulation_data.csv'
    df.to_csv(path)

path = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/bulk_simulation_data.csv'
df.to_csv(path)
