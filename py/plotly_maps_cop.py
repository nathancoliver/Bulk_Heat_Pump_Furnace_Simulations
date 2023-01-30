import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


def call_file(path):
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    return df


path1 = '/Users/nathanoliver/Desktop/Python/Bulk_Simulations_ASHP_Furnace/csv/bulk_simulation_results_heatmap_no_outliers.csv'

df = call_file(path1)

for i in range(len(df)):
    if df.loc[i, 'FIPS'] < 10000:
        df.loc[i, 'FIPS'] = '0' + str(df.loc[i, 'FIPS'])
        # print(df.loc[i, 'FIPS'])
    else:
        pass
        # df.loc[i, 'fips'] = str(df.loc[i, 'fips'])
        # print(df.loc[i, 'fips'])




cop = df['h1_cop'].tolist()
fips = df['FIPS'].tolist()

low = min(cop)
hgh = max(cop)

print(low,hgh)


scope = ['usa']



colorscale =['#de425b',
'#e76b77',
'#ee8e94',
'#f2afb2',
'#f3d0d1',
'#f1f1f1',
'#c8c1d6',
'#9f93bd',
'#7768a3',
'#4d3f89',
'#191970']

grey = '#A9A9A9'

colorscale =['#de425b',
'#e66572',
'#ec838a',
'#f09fa2',
'#f3babc',
'#f3d6d6',
'#f1f1f1',
'#cec9db',
'#aca2c5',
'#8b7db0',
'#695a9a',
'#453985',
'#191970',
grey]

colorscale.reverse()




binning_endpoints = []

dec = 6
n = 1

for i in range(len(colorscale) - n):
    if i == 0:
        binning_endpoints.append(round(low, dec))
    elif i == len(colorscale) - n - 1:
        binning_endpoints.append(round(hgh, dec))
    else:
        binning_endpoints.append(round(
            low + (hgh - low) * i / (len(colorscale) - n - 1), dec))

print(binning_endpoints)

binning_endpoints = [0,1.5,1.7,1.9,2.1,2.3,2.5,2.7,2.9,3.1,3.3,3.5,4.5]

# binning_endpoints = [0, 14348, 63983, 134827, 426762, 2081313]

# binning_endpoints = np.arange()

title = 'Heat Pump COP'
legend_title = ''


fig = ff.create_choropleth(

    fips=fips,
    values=cop,
    scope=scope,
    colorscale=colorscale,
    binning_endpoints=binning_endpoints,
    title_text=title,
    legend_title=legend_title,
    round_legend_values=False,
    county_outline={'color': 'black', 'width': 0.2},
    state_outline={'color': 'black', 'width': 1}
)

fig.show()
