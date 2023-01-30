import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


def call_file(path):
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    return df

path1 = '/Users/nathanoliver/Desktop/Python/Bulk_Simulations_ASHP_Furnace/csv/bulk_simulation_results.csv'
path2 = '/Users/nathanoliver/Desktop/Python/Bulk_Simulations_ASHP_Furnace/csv/Subregion_Number.csv'

df1 = call_file(path1)
df2 = call_file(path2)

# for i in range(len(df1)):
#     subgrid = df1.loc[i,'SUBGRID']
#     index = df2.index[df2['region'] == subgrid][0]
#     df1.loc[i,'SUBGRID'] = df2.loc[index,'number']




subgrid = df1['SUBGRID'].tolist()
fips = df1['FIPS'].tolist()

scope = ['usa']

grey = '#A9A9A9'



colorscale = ['#488f31',
'#78ab63',
'#a5c796',
'#d2e3c9',
'#fcd1d0',
'#f3a3a4',
'#e67379',
'#d43d51']

colorscale = ['#00876c',
'#469b83',
'#6eaf9a',
'#93c3b3',
'#b7d7cc',
'#dbebe5',
'#fde0e0',
'#f9c2c1',
'#f3a3a4',
'#eb8387',
'#e0636b',
'#d43d51']

colorscale = ['#17746f',
'#17746f',
'#879d5c',
'#aae82e',
'#fbb823',
'#29b4e9',
'#17746f',
'#17746f',
'#17746f',
'#cf27ff',
'#54b325',
'#fefd26',
'#c88883',
'#abb7de',
'#fcecb8',
'#2cb293',
'#e92529',
'#6ffe26',
'#2785ff',
'#fc9393',
'#ffc7ec',
'#df8afb',
'#fefe86',
'#c8ffec',
'#a2b528',
'#ff6f28']


# binning_endpoints = []

# dec = 6

# for i in range(len(colorscale) - n):
#     if i == 0:
#         binning_endpoints.append(round(low, dec))
#     elif i == len(colorscale) - n - 1:
#         binning_endpoints.append(round(hgh, dec))
#     else:
#         binning_endpoints.append(round(
#             low + (hgh - low) * i / (len(colorscale) - n - 1), dec))

# print(binning_endpoints)

binning_endpoints = [-.5,-.4,-.3,-.2,-.1,0,.1,.2,.3,.4,.5]

# binning_endpoints = [0, 14348, 63983, 134827, 426762, 2081313]

# binning_endpoints = np.arange()

title = 'Subgrids'
legend_title = ''


fig = ff.create_choropleth(

    fips=fips,
    values=subgrid,
    scope=scope,
    colorscale=colorscale,
    # binning_endpoints=binning_endpoints,
    title_text=title,
    legend_title=legend_title,
    # round_legend_values=True,
    county_outline={'color': 'black', 'width': 0.2},
    state_outline={'color': 'black', 'width': 1}
)

fig.show()
