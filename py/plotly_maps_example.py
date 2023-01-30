import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


def call_file(path):
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    return df


path1 = '/Users/nathanoliver/Desktop/Cancer Rates/csv/06_csv_cancer_rates/cancer_rates.csv'
path2 = '/Users/nathanoliver/Desktop/Cancer Rates/csv/07_fips/fips.csv'

df = call_file(path1)
df5 = call_file(path2)

for i in range(len(df5)):
    if df5.loc[i, 'fips'] < 10000:
        df5.loc[i, 'fips'] = '0' + str(df5.loc[i, 'fips'])
        print(df5.loc[i, 'fips'])
    else:
        pass
        # df.loc[i, 'fips'] = str(df.loc[i, 'fips'])
        # print(df.loc[i, 'fips'])

# print(df['cancer'].unique())
# print(df['race'].unique())
# print(df['sex'].unique())
# print(df['age'].unique())


title = 'Melanoma Incidence Rates by US County, 2015-2019'
legend_title = 'Incidence Rate per 100,000'
# df1 = df[df['cancer'] == 'Lung & Bronchus']
df1 = df[df['cancer'] == 'Melanoma of the Skin']
df2 = df1[df1['race'] == 'All Races']
df3 = df2[df2['sex'] == 'Both Sexes']
df4 = df3[df3['age'] == 'All Ages']

rate = df4['incidence_rate'].tolist()
fips = df4['fips'].tolist()

# low = 29.4
# hgh = 848.8

low = min(rate)
hgh = max(rate)

n = len(df4)

for i in range(len(df5)):

    val = df5.loc[i, 'fips']

    if val not in df4['fips']:
        new_row = {'county': 0, 'state': 0, 'cancer': 0, 'race': 0, 'sex': 0, 'age': 0,
                   'incidence_rate': 0, 'lower_95%': 0, 'upper_95%': 0, 'average_annual_count': 0, 'fips': val}
        df4 = df4.append(new_row, ignore_index=True)
        # df4.loc[n]=0,0,0,0,0,0,0,0,0,0,val
        print(val)

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

colorscale = ['#540026',
              '#650023',
              '#76001D',
              '#870014',
              '#970009',
              '#A50000',
              '#B30A00',
              '#C02000',
              '#CD3802',
              '#D95206',
              '#E46E0A',
              '#EB792C',
              '#F0874F',
              '#F59973',
              '#F9AF99',
              grey]

colorscale.reverse()

# colorscale = ['#004c6d',
# '#14688b',
# '#2686a8',
# '#38a5c6',
# '#4cc5e3',
# '#61e6ff']

rate = df4['incidence_rate'].tolist()
fips = df4['fips'].tolist()

# low = 29.4
# hgh = 848.8

# low = min(rate)
# hgh = max(rate)


n = 1
print('length of colors: ', len(colorscale))

binning_endpoints = []

for i in range(len(colorscale) - n):
    if i == 0:
        binning_endpoints.append(round(low, 0))
    elif i == len(colorscale) - n - 1:
        binning_endpoints.append(round(hgh, 0))
    else:
        binning_endpoints.append(round(
            low + (hgh - low) * i / (len(colorscale) - n - 1), 0))

print(binning_endpoints)


# binning_endpoints = [0, 14348, 63983, 134827, 426762, 2081313]

# binning_endpoints = np.arange()


fig = ff.create_choropleth(

    fips=fips,
    values=rate,
    scope=scope,
    colorscale=colorscale,
    binning_endpoints=binning_endpoints,
    title_text=title,
    legend_title=legend_title,
    round_legend_values=True,
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}
)

fig.show()
