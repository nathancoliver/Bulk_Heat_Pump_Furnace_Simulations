import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


def call_file(path):
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    return df

path1 = '/Users/nathanoliver/Desktop/Python/Bulk_Simulations_ASHP_Furnace/csv/bulk_simulation_results_heatmap.csv'


df1 = call_file(path1)


# for i in range(len(df1)):
#     subgrid = df1.loc[i,'SUBGRID']
#     index = df2.index[df2['region'] == subgrid][0]
#     df1.loc[i,'SUBGRID'] = df2.loc[index,'number']




elec_price = df1['elec_price'].tolist()
fips = df1['FIPS'].tolist()


low = min(elec_price)
hgh = max(elec_price)

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

binning_endpoints = [10,15,20,25,30,35,40,45,50]

# binning_endpoints = [0, 14348, 63983, 134827, 426762, 2081313]

# binning_endpoints = np.arange()

title = 'Subgrids'
legend_title = ''


fig = ff.create_choropleth(

    fips=fips,
    values=elec_price,
    scope=scope,
    colorscale=colorscale,
    binning_endpoints=binning_endpoints,
    title_text=title,
    legend_title=legend_title,
    simplify_county=0.001,
    # round_legend_values=True,
    # county_outline={'color': 'black', 'width': 0},
    state_outline={'color': 'black', 'width': 1}
)

fig.show()
