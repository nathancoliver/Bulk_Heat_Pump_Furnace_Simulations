import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


def call_file(path):
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    return df


path1 = '/Users/nathanoliver/Desktop/Python/Bulk_Simulations_ASHP_Furnace/csv/bulk_simulation_results.csv'

df = call_file(path1)

for i in range(len(df)):
    if df.loc[i, 'FIPS'] < 10000:
        df.loc[i, 'FIPS'] = '0' + str(df.loc[i, 'FIPS'])
        # print(df.loc[i, 'FIPS'])
    else:
        pass
        # df.loc[i, 'fips'] = str(df.loc[i, 'fips'])
        # print(df.loc[i, 'fips'])

# print(df['cancer'].unique())
# print(df['race'].unique())
# print(df['sex'].unique())
# print(df['age'].unique())


emissions = df['emissions_comparison'].tolist()
cost = df['cost_comparison'].tolist()
fips = df['FIPS'].tolist()

# low = 29.4
# hgh = 848.8

cost_low = min(cost)
cost_high = max(cost)

# n = len(df4)

# for i in range(len(df5)):

#     val = df5.loc[i, 'fips']

#     if val not in df4['fips']:
#         new_row = {'county': 0, 'state': 0, 'cancer': 0, 'race': 0, 'sex': 0, 'age': 0,
#                    'incidence_rate': 0, 'lower_95%': 0, 'upper_95%': 0, 'average_annual_count': 0, 'fips': val}
#         df4 = df4.append(new_row, ignore_index=True)
#         # df4.loc[n]=0,0,0,0,0,0,0,0,0,0,val
#         print(val)

scope = ['usa']

# colorscale = [
#     'rgb(193, 193, 193)',
#     'rgb(239,239,239)',
#     'rgb(195, 196, 222)',
#     'rgb(144,148,194)',
#     'rgb(101,104,168)',
#     'rgb(65, 53, 132)'
# ]

# colorscale = ['#e2e2e2',
#               '#e5c9c8',
#               '#e6afaf',
#               '#e49596',
#               '#e17b7e',
#               '#db5e67',
#               '#d43d51']

# colorscale = ['#00876c',
# '#6eaf9a',
# '#b7d7cc',
# '#ffffff',
# '#f9c2c1',
# '#eb8387',
# '#d43d51']

colorscale = ['#488f31'
,'#76a263'
,'#9fb494'
,'#c6c6c6'
,'#d39d9d'
,'#d77276'
,'#d43d51']

# colorscale = ['#0A2F51',
#               '#0E4D64',
#               '#137177',
#               '#188977',
#               '#1D9A6C',
#               '#39A96B',
#               '#56B870',
#               '#74C67A',
#               '#99D492',
#               '#BFE1B0',
#               '#DEEDCF']

grey = '#A9A9A9'

'#FCC9BF'

# colorscale = ['#540026',
#               '#650023',
#               '#76001D',
#               '#870014',
#               '#970009',
#               '#A50000',
#               '#B30A00',
#               '#C02000',
#               '#CD3802',
#               '#D95206',
#               '#E46E0A',
#               '#EB792C',
#               '#F0874F',
#               '#F59973',
#               '#F9AF99',
#               grey]

# colorscale.reverse()

# colorscale = ['#004c6d',
# '#14688b',
# '#2686a8',
# '#38a5c6',
# '#4cc5e3',
# '#61e6ff']

# rate = df4['emissions'].tolist()
# fips = df4['fips'].tolist()

# low = 29.4
# hgh = 848.8

# colorscale = ['#488f31',
# '#78ab63',
# '#a5c796',
# '#d2e3c9',
# '#fcd1d0',
# '#f3a3a4',
# '#e67379',
# '#d43d51']


# colorscale = ['#00876c',
# '#469b83',
# '#6eaf9a',
# '#93c3b3',
# '#b7d7cc',
# '#dbebe5',
# '#fde0e0',
# '#f9c2c1',
# '#f3a3a4',
# '#eb8387',
# '#e0636b',
# '#d43d51']


colorscale = [
'#00876c',
# '#469b83',
'#6eaf9a',
# '#93c3b3',
'#b7d7cc',
# '#dbebe5',
# '#fde0e0',
'#f9c2c1',
# '#f3a3a4',
'#eb8387',
# '#e0636b',
'#d43d51']


low = min(cost)
hgh = max(cost)


n = 1
print('length of colors: ', len(colorscale))

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

# binning_endpoints = [-.5,-.4,-.3,-.2,-.1,0,.1,.2,.3,.4,.5]
binning_endpoints = [-.4,-.2,0,.2,.4]

# binning_endpoints = [0, 14348, 63983, 134827, 426762, 2081313]

# binning_endpoints = np.arange()

title = 'Percent Change in Energy Cost of Air-Source Heat Pump\nRelative to Natural Gas Furnace'
legend_title = 'Percent Change'


fig = ff.create_choropleth(

    fips=fips,
    values=cost,
    scope=scope,
    colorscale=colorscale,
    binning_endpoints=binning_endpoints,
    title_text=title,
    legend_title=legend_title,
    round_legend_values=False,
    county_outline={'color': 'black', 'width': 0.2},
    state_outline={'color': 'black', 'width': 1}
)

fig.update_layout(title={'x':0.5})
# fig.update_layout(
#     legend=dict(
#         x=0,
#         y=1,
#         title_font_family="Times New Roman",
#         font=dict(
#             family="Courier",
#             size=12,
#             color="black"
#         ),
#         bgcolor="LightBlue",
#         bordercolor="Black",
#         borderwidth=1
#     )
# )

fig.show()
