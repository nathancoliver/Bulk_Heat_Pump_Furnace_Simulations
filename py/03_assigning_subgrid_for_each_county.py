import pandas as pd
import numpy as np

def read_file(path):
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    return df

path1 = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/ZIP-COUNTY-FIPS_2018-03.csv'
path2 = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/STATE_ABR_FIPS.csv'
path3 = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/EPW_FIPS_ZIP_CODES.csv'
path4 = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/ZIP_SUBREGION.csv'

df1 = read_file(path1)
df2 = read_file(path2)
df3 = read_file(path3)
df4 = read_file(path4)

county_fip = df1.loc[0,'STCOUNTYFP']

print(df1.info())
print(df2.info())

print(county_fip)

df4['zip']=df4['zip'].apply(lambda x: '{0:0>5}'.format(x))
df1['STCOUNTYFP']=df1['STCOUNTYFP'].apply(lambda x: '{0:0>5}'.format(x))

for i in range(len(df3)):
    fips = df3.loc[i,'FIPS']
    print(fips)
    df3.loc[i,'FIPS'] = str(fips[2:7])

print(df3['FIPS'])

print(df4['zip'])
print(df1['STCOUNTYFP'])

df3['SUBGRID'] = ''


print(df3)
print('subgrid',df3.loc[0,'SUBGRID'])


for n in range(len(df3)):
    # for n in range(1):
    # fips = '01001'
    fips = df3.loc[n,'FIPS']
    print(fips)
    df1_single_fip = df1[df1['STCOUNTYFP'] == fips]
    df1_single_fip = df1_single_fip.reset_index()
    # print(df1_single_fip)

    for q in range(len(df1_single_fip)):
        # print(q)
        # print(df1_single_fip.loc[q,'ZIP'])
        zip_code = df1_single_fip.loc[q,'ZIP']

        if zip_code < 10000:
            zip_code = '0'+str(zip_code)
            index = df4.index[df4['zip'] == str(zip_code)]
        else:
            index = df4.index[df4['zip'] == str(zip_code)]
        # print(zip_code)

        # print(index)
        try:
            subgrid = df4.loc[index[0],'SUBREGION_1']
        except:
            pass

        df1_single_fip.loc[q,'SUBGRID'] = subgrid

        # print(subgrid)

    print(df1_single_fip)

    try:
        print(df1_single_fip['SUBGRID'].value_counts().idxmax())
        df3.loc[n,'SUBGRID'] = df1_single_fip['SUBGRID'].value_counts().idxmax()
    except:
        df3.loc[n,'SUBGRID'] = 0

    del df1_single_fip

path = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/new_file.csv'
df3.to_csv(path)








