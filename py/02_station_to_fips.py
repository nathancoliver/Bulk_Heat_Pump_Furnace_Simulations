import pandas as pd
import numpy as np

def read_file(path):
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    return df

path = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/ZIP_CODES_final.csv'

df = read_file(path)

print(df.info())

for n in range(len(df)):
    station = df.loc[n,'Station_Number']
    df.loc[n,'FIPS'] = station[1:3]+station[4:7]

print(df['FIPS'])

# df['FIPS'] = df['FIPS'].astype('str')
df['FIPS'] = df['FIPS'].apply('="{}"'.format)

path_csv = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/EPW_FIPS_ZIP_CODES.csv'

df.to_csv(path_csv)
