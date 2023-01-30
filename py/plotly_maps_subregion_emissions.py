import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


def call_file(path):
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    return df

path1 = '/Users/nathanoliver/Desktop/Python/Bulk_Simulations_ASHP_Furnace/csv/bulk_simulation_results_heatmap.csv'
path2 = '/Users/nathanoliver/Desktop/Python/Bulk_Simulations_ASHP_Furnace/csv/Subregion_Number.csv'

df1 = call_file(path1)
df2 = call_file(path2)

# for i in range(len(df1)):
#     subgrid = df1.loc[i,'SUBGRID']
#     index = df2.index[df2['region'] == subgrid][0]
#     df1.loc[i,'SUBGRID'] = df2.loc[index,'number']




subgrid = df1['grid_emissions_metric_tons_MMBtu'].tolist()
fips = df1['FIPS'].tolist()


low = min(subgrid)
hgh = max(subgrid)

scope = ['usa']

grey = '#A9A9A9'



# colorscale = ['#004c6d',
# '#346888',
# '#5886a5',
# '#7aa6c2',
# '#9dc6e0',
# '#c1e7ff']

colorscale = ['#00876c',
'#4c9c85',
'#78b19f',
'#a0c6b9',
'#c8dbd5',
# '#f1f1f1',
'#f1cfce',
'#eeadad',
'#e88b8d',
'#df676e',
'#d43d51']

print(len(colorscale))
binning_endpoints = []
n = 1
dec = 6

for i in range(len(colorscale) - n):
    if i == 0:
        binning_endpoints.append(round(low, dec))
    elif i == len(colorscale) - n - 1:
        binning_endpoints.append(round(hgh, dec))
    else:
        binning_endpoints.append(round(
            low + (hgh - low) * i / (len(colorscale) - n - 1), dec))

print(len(binning_endpoints))

binning_endpoints = [40,60,80,100,120,140,160,180,200]

# binning_endpoints = [0, 14348, 63983, 134827, 426762, 2081313]

# binning_endpoints = np.arange()

title = 'Subgrids'
legend_title = ''


fig = ff.create_choropleth(

    fips=fips,
    values=subgrid,
    scope=scope,
    colorscale=colorscale,
    binning_endpoints=binning_endpoints,
    title_text=title,
    legend_title=legend_title,
    # round_legend_values=True,
    county_outline={'color': 'black', 'width': 0.2},
    state_outline={'color': 'black', 'width': 1}
)

fig.show()
