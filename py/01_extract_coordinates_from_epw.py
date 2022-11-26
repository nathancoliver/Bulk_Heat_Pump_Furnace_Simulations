import geopy
import pandas as pd
import csv
import numpy as np

# extract coordinates of weather stations from epw file

geolocator = geopy.Nominatim(user_agent='what')

# definition to call geopy with coordinates and obtain zipcodes
def get_zipcode(geolocator, lat_field, lon_field):
    location = geolocator.reverse((lat_field, lon_field))

    try:
        return location.raw['address']['postcode']
    except Exception:
         return None

# def get_zipcode(df, geolocator, lat_field, lon_field):
#     location = geolocator.reverse((df[lat_field], df[lon_field]))
#     return location.raw['address']['postcode']


def state_zipcodes(num):
    station_state = []
    station_name = []
    station_wmo = []
    station_num = []
    station_lat = []
    station_lng = []
    station_zip = []


    # epw weather file path





    for n in range(len(num)):
        exit = 0
        if num[n] < 1000000:
            path = 'C:/Users/nathan.oliver/Desktop/Energy_Plus_Weather_Files/G0'
            new_path = path + str(num[n]) + '.epw'

        else:
            path = 'C:/Users/nathan.oliver/Desktop/Energy_Plus_Weather_Files/G'
            new_path = path + str(num[n]) + '.epw'

        try:
            with open(new_path) as csv_file:
                csv_reader = csv.reader(csv_file)
                rows = list(csv_reader)
        except:
            continue

        header = rows[0]

        name = header[1]
        state = header[2]
        print(state)
        wmo = header[5]
        lat = header[6]
        lng = header[7]

        print(lat,lng)

        station_state.append(state)
        station_name.append(name)
        station_wmo.append(wmo)
        if num[n] < 1000000:
            station_num.append('G0'+ str(num[n]))
        else:
            station_num.append('G'+ str(num[n]))
        station_lat.append(float(lat))
        station_lng.append(float(lng))




        # df = pd.DataFrame({
        #     'Lat': float(lat),
        #     'Lon': float(lng)
        # })

        zip_code = get_zipcode(geolocator = geolocator, lat_field = float(lat), lon_field = float(lng))

        if zip_code is None:
            station_zip.append(zip_code)
            print(zip_code)
        else:
            station_zip.append(zip_code[:5])
            print(zip_code[:5])

        df = pd.DataFrame({'State': station_state,
            'Station_Number': station_num,
            'Station_Name': station_name,
            'Station_WMO': station_wmo,
            'Latitude': station_lat,
            'Longitude': station_lng,
            'ZIP Codes': station_zip
        })

    # print(df)

        path_csv = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/ZIP_CODES5.csv'

        df.to_csv(path_csv)

    return df.to_csv(path_csv)

x = state_zipcodes(num = np.arange(2601060,5600450+10,10))
# x = state_zipcodes(state = 'AL', num = np.arange(100010,101330+20,20))
# x = state_zipcodes(state = 'AZ', num = np.arange(400030,400270+20,20))
# x = state_zipcodes(state = 'AR', num = np.arange(500010,501490+20,20))
# x = state_zipcodes(state = 'CA', num = np.arange(600010,601150+20,20))
# x = state_zipcodes(state = 'MN', num = np.arange(2700010,2701750,20))
