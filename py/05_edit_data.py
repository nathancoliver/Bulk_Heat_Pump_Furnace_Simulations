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

# path = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/new_file_energy_Madison.csv'
# path = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/new_file_energy_WI_new_file.csv'
path = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/bulk_simulation_data.csv'
path2 = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/STATE_ABR_FIPS.csv'
path3 = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/US_Region_Electricity_Emissions_2019.csv'
path4 = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/US_State_Electricity_NG_Prices.csv'

df = read_file(path)
df_state_fips = read_file(path2)
df_subgrid = read_file(path3)
df_price = read_file(path4)

# column = ['STATE','h1_emissions','c1_emissions','t1_emissions','h2_emissions','c2_emissions','t2_emissions','h1_cost','c1_cost','t1_cost','h2_cost','c2_cost','t2_cost']

# for col in column:
#     df[col] = ''

df['FIPS'] = df['FIPS'].astype(str)

for i in range(len(df)):
    fips = df.loc[i,'FIPS']
    if int(fips) < 10000:
        state_fips = fips[:1]
    else:
        state_fips = fips[:2]

    # print(state_fips)

    state_index = df_state_fips.index[df_state_fips['FIPS'] == int(state_fips)]

    print(state_index[0])

    df.loc[i,'STATE'] = df_state_fips.loc[state_index[0], 'Postal Code']


# h1 and c1 are heating and cooling for point 1 (Heat Pump)
# h2 and c2 are heating and cooling for point 2 (AC unit and NG Furnace)

# Heat Pump Emissions - Heating
# sub-grid emissions rate x electricity site usage (el_sit_h1 + el_sit_sub_h1) / (1 - transmission losses / 100) x conversion

# Heat Pump Emissions - Cooling
# sub-grid emissions rate x electricity site usage (el_sit_c1 + el_sit_sub_c1) / (1 - transmission losses / 100) x conversion

# Furnace Emissions - Heating
# ng site usage (ng_sit_h2) x conversion x 52.91 / 1000

# AC Emissions - Cooling
# sub-grid emissions rate x electricity site usage (el_sit_c2 + el_sit_sub_c2) / (1 - transmission losses / 100) x conversion

# Heat Pump Cost - Heating
# electricity site usage (el_sit_h1) * rate

# Heat Pump Cost - Cooling
# electricity site usage (el_sit_c1) * rate

# Furnace Cost - Heating
# natural gas site usage (ng_sit_h2) * rate

# Furnace Cost - Heating
# electricity site usage (el_sit_c2) * rate


# AC Emissions - Cooling


# conversion 1 one-million British Thermal Unit to megajoules = 1,055.06 MJ

conversion_MJ_to_MMBtu = 1/1055.06
ng_emissions = 52.91

for i in range(len(df)):
    sub_grid = df.loc[i,'SUBGRID']
    state = df.loc[i,'STATE']

    sub_grid_index = df_subgrid.index[df_subgrid['region'] == sub_grid][0]

    state_index = df_price.index[df_price['State_Abbreviation'] == state][0]


    sub_grid_emissions = df_subgrid.loc[sub_grid_index,'co2e (metric tons / MMBtu)']
    sub_grid_elec_losses = df_subgrid.loc[sub_grid_index,'elec_loss']

    state_elec_price  = df_price.loc[state_index,'Electricity ($/MMBtu)']
    state_ng_price = df_price.loc[state_index,'Natural Gas ($/MMBtu)']

    # print(sub_grid_emissions, sub_grid_elec_losses)

    # Heat Pump emissions - Heating and Cooling (see equations above)
    df.loc[i,'h1_emissions'] = (df.loc[i,'el_sit_h1'] + df.loc[i,'el_sit_sub_h1']) * conversion_MJ_to_MMBtu * sub_grid_emissions / (1-sub_grid_elec_losses/100)
    # df.loc[i,'c1_emissions'] = (df.loc[i,'el_sit_c1'] + df.loc[i,'el_sit_sub_c1'])*conversion_MJ_to_MMBtu*sub_grid_emissions/(1-sub_grid_elec_losses/100)
    df.loc[i,'c1_emissions'] = df.loc[i,'el_sit_c1'] * conversion_MJ_to_MMBtu * sub_grid_emissions / (1-sub_grid_elec_losses / 100)
    df.loc[i,'t1_emissions'] = df.loc[i,'h1_emissions'] + df.loc[i,'c1_emissions']
    # df.loc[i,'t1_el_emissions'] = df.loc[i,'el_sit_t1'] * conversion_MJ_to_MMBtu * sub_grid_emissions / (1-sub_grid_elec_losses / 100)
    # df.loc[i,'t1_ng_emissions'] = df.loc[i,'ng_sit_t1'] * conversion_MJ_to_MMBtu * 52.91 / 1000
    # df.loc[i,'t1_emissions'] = df.loc[i,'t1_el_emissions'] + df.loc[i,'t1_ng_emissions']


    # print(df.loc[i,'h1_emissions'],df.loc[i,'c1_emissions'],df.loc[i,'t1_emissions'])

    # AC/NG Furnace emissions - Heating and Cooling (see equations above)
    # ng site usage (ng_sit_h2) x conversion x 52.91 / 1000
    df.loc[i,'h2_emissions'] = df.loc[i,'ng_sit_h2'] * conversion_MJ_to_MMBtu * 52.91 / 1000
    # df.loc[i,'c2_emissions'] = (df.loc[i,'el_sit_c2'] + df.loc[i,'el_sit_sub_c2'])*conversion_MJ_to_MMBtu*sub_grid_emissions/(1-sub_grid_elec_losses/100)
    df.loc[i,'c2_emissions'] = df.loc[i,'el_sit_c2'] * conversion_MJ_to_MMBtu * sub_grid_emissions / (1-sub_grid_elec_losses / 100)
    df.loc[i,'t2_emissions'] = df.loc[i,'h2_emissions'] + df.loc[i,'c2_emissions']
    # df.loc[i,'t2_el_emissions'] = df.loc[i,'el_sit_t2'] * conversion_MJ_to_MMBtu * sub_grid_emissions / (1-sub_grid_elec_losses / 100)
    # df.loc[i,'t2_ng_emissions'] = df.loc[i,'ng_sit_t2'] * conversion_MJ_to_MMBtu * 52.91 / 1000
    # df.loc[i,'t2_emissions'] = df.loc[i,'t2_el_emissions'] + df.loc[i,'t1_ng_emissions']


    # print(df.loc[i,'h2_emissions'],df.loc[i,'c2_emissions'],df.loc[i,'t2_emissions'])


    # Heat Pump cost - Heating and Cooling (see equations above)
    df.loc[i,'h1_cost'] = df.loc[i,'el_sit_h1'] * conversion_MJ_to_MMBtu * state_elec_price
    df.loc[i,'c1_cost'] = df.loc[i,'el_sit_c1'] * conversion_MJ_to_MMBtu * state_elec_price
    df.loc[i,'t1_cost'] = df.loc[i,'h1_cost'] + df.loc[i,'c1_cost']
    # df.loc[i,'t1_cost_el'] = df.loc[i,'el_sit_t1'] * conversion_MJ_to_MMBtu * state_elec_price
    # df.loc[i,'t1_cost_ng'] = df.loc[i,'ng_sit_t1'] * conversion_MJ_to_MMBtu * state_ng_price
    # df.loc[i,'t1_cost'] = df.loc[i,'t1_cost_el'] + df.loc[i,'t1_cost_ng']

    # AC/NG Furnace cost - Heating and Cooling (see equations above)
    df.loc[i,'h2_cost'] = df.loc[i,'ng_sit_h2'] * conversion_MJ_to_MMBtu * state_ng_price
    df.loc[i,'c2_cost'] = df.loc[i,'el_sit_c2'] * conversion_MJ_to_MMBtu * state_elec_price
    df.loc[i,'t2_cost'] = df.loc[i,'h2_cost'] + df.loc[i,'c2_cost']
    # df.loc[i,'t2_cost_el'] = df.loc[i,'el_sit_t2'] * conversion_MJ_to_MMBtu * state_elec_price
    # df.loc[i,'t2_cost_ng'] = df.loc[i,'ng_sit_t2'] * conversion_MJ_to_MMBtu * state_ng_price
    # df.loc[i,'t2_cost'] = df.loc[i,'t2_cost_el'] + df.loc[i,'t2_cost_ng']

    # print(df.loc[i,'h1_cost'],df.loc[i,'c1_cost'],df.loc[i,'t1_cost'])
    # print(df.loc[i,'h2_cost'],df.loc[i,'c2_cost'],df.loc[i,'t2_cost'])
    # print('')
    # print(df.loc[i,'el_sit_h1'],df.loc[i,'el_sit_c1'])
    # print(df.loc[i,'ng_sit_h2'],df.loc[i,'el_sit_c2'])
    # print(state_ng_price,state_elec_price)
    # print('')

    # Heat Pump COP - Heating

    # try:
    #     df.loc[i,'h1_cop'] = df.loc[i,'el_del_h1'] / df.loc[i,'el_sit_h1']
    # except:
    #     pass
    # print(df.loc[i,'h1_cop'])

    df.loc[i,'emissions_comparison'] = (df.loc[i,'t1_emissions'] - df.loc[i,'t2_emissions']) / df.loc[i,'t2_emissions']
    df.loc[i,'cost_comparison'] = (df.loc[i,'t1_cost'] - df.loc[i,'t2_cost']) / df.loc[i,'t2_cost']
    # print(df.loc[i,'emissions_comparison'],sub_grid,df.loc[i,'h1_cop'],df.loc[i,'cost_comparison'])

    # path = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/bulk_simulation_results.csv'
    # df.to_csv(path)
path = 'C:/Users/nathan.oliver/Desktop/Python/Heat_Pump_Furnace_EPlus_Batch_Simulations/csv/bulk_simulation_results.csv'
df.to_csv(path)
