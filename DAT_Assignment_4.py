import numpy
import pandas
import seaborn
from scipy import stats
import statsmodels.api as stats_models_api
import matplotlib.pyplot as pyplot

# read from dataset
data = pandas.read_csv('dataset/marscrater_pds.csv', low_memory=False)

# bug fix for display formats to avoid run time errors
pandas.set_option('display.float_format', lambda x:'%f'%x)

# setting variables to numeric
data['DIAM_CIRCLE_IMAGE'] = pandas.to_numeric(data['DIAM_CIRCLE_IMAGE'], errors='coerce')
data['DEPTH_RIMFLOOR_TOPOG'] = pandas.to_numeric(data['DEPTH_RIMFLOOR_TOPOG'], errors='coerce')
data['LATITUDE_CIRCLE_IMAGE'] = pandas.to_numeric(data['LATITUDE_CIRCLE_IMAGE'], errors='coerce')

# choosen subset to work with
working_subset_1 = data[
    (data['NUMBER_LAYERS'] > 0) & (data['DIAM_CIRCLE_IMAGE'] > 0) & (data['DIAM_CIRCLE_IMAGE'] <= 100)
    & (data['DEPTH_RIMFLOOR_TOPOG'] > 0) & (data['DEPTH_RIMFLOOR_TOPOG'] <= 3)
]

working_subset_2 = working_subset_1.copy()


def MARS_REGION(row):
    if row['LATITUDE_CIRCLE_IMAGE'] > 45:
        return 1
    elif 0 <= row['LATITUDE_CIRCLE_IMAGE'] <= 45:
        return 2
    elif 0 > row['LATITUDE_CIRCLE_IMAGE'] >= -45:
        return 3
    elif row['LATITUDE_CIRCLE_IMAGE'] < -45:
        return 4

working_subset_2['MARS_REGION'] = working_subset_2.apply(lambda row: MARS_REGION(row), axis=1)

# checking for missing data
check_1 = working_subset_2['MARS_REGION'].value_counts(sort=False, dropna=False)
print(check_1)
print()
print()

working_subset_3 = working_subset_2[(working_subset_2['MARS_REGION'] == 1)]
working_subset_4 = working_subset_2[(working_subset_2['MARS_REGION'] == 2)]
working_subset_5 = working_subset_2[(working_subset_2['MARS_REGION'] == 3)]
working_subset_6 = working_subset_2[(working_subset_2['MARS_REGION'] == 4)]

# calculate p-value & r-value for each region
print('Association between CRATER DIAMETER and CRATER DEPTH without a moderator')
print(stats.pearsonr(working_subset_2['DIAM_CIRCLE_IMAGE'], working_subset_2['DEPTH_RIMFLOOR_TOPOG']))
print()
print()

print('Association between CRATER DIAMETER and CRATER DEPTH for North Pole')
print(stats.pearsonr(working_subset_3['DIAM_CIRCLE_IMAGE'], working_subset_3['DEPTH_RIMFLOOR_TOPOG']))
print()
print()

print('Association between CRATER DIAMETER and CRATER DEPTH for Upper Equator')
print(stats.pearsonr(working_subset_4['DIAM_CIRCLE_IMAGE'], working_subset_4['DEPTH_RIMFLOOR_TOPOG']))
print()
print()

print('Association between CRATER DIAMETER and CRATER DEPTH for Lower Equator')
print(stats.pearsonr(working_subset_5['DIAM_CIRCLE_IMAGE'], working_subset_5['DEPTH_RIMFLOOR_TOPOG']))
print()
print()

print('Association between CRATER DIAMETER and CRATER DEPTH for South Pole')
print(stats.pearsonr(working_subset_6['DIAM_CIRCLE_IMAGE'], working_subset_6['DEPTH_RIMFLOOR_TOPOG']))
print()
print()

# creating graph visually for each region
graph_1 = seaborn.lmplot(x='DIAM_CIRCLE_IMAGE', y='DEPTH_RIMFLOOR_TOPOG', fit_reg=True, scatter_kws={'color': 'darkblue'}, line_kws={'color': 'red'}, data=working_subset_2)
pyplot.xlabel('Crater Diameter (km)')
pyplot.ylabel('Crater Depth (km)')
pyplot.title('Relationship between Crater Diameter & Crater Depth without a moderator')
graph_1.set(xlim=(0, 120))
graph_1.set(ylim=(0, 4))
pyplot.xticks(numpy.arange(0, 120+20, 20))
pyplot.yticks(numpy.arange(0, 5+1, 1))
pyplot.tick_params(axis='both')
pyplot.show()


graph_2 = seaborn.lmplot(x='DIAM_CIRCLE_IMAGE', y='DEPTH_RIMFLOOR_TOPOG', fit_reg=True, scatter_kws={'color': 'darkblue'}, line_kws={'color': 'red'}, data=working_subset_3)
pyplot.xlabel('Crater Diameter (km)')
pyplot.ylabel('Crater Depth (km)')
pyplot.title('Relationship between Crater Diameter & Crater Depth for North Pole')
graph_2.set(xlim=(0, 120))
graph_2.set(ylim=(0, 4))
pyplot.xticks(numpy.arange(0, 120+20, 20))
pyplot.yticks(numpy.arange(0, 5+1, 1))
pyplot.tick_params(axis='both')
pyplot.show()


graph_3 = seaborn.lmplot(x='DIAM_CIRCLE_IMAGE', y='DEPTH_RIMFLOOR_TOPOG', fit_reg=True, scatter_kws={'color': 'darkblue'}, line_kws={'color': 'red'}, data=working_subset_4)
pyplot.xlabel('Crater Diameter (km)')
pyplot.ylabel('Crater Depth (km)')
pyplot.title('Relationship between Crater Diameter & Crater Depth for Upper Equator')
graph_3.set(xlim=(0, 120))
graph_3.set(ylim=(0, 4))
pyplot.xticks(numpy.arange(0, 120+20, 20))
pyplot.yticks(numpy.arange(0, 5+1, 1))
pyplot.tick_params(axis='both')
pyplot.show()


graph_4 = seaborn.lmplot(x='DIAM_CIRCLE_IMAGE', y='DEPTH_RIMFLOOR_TOPOG', fit_reg=True, scatter_kws={'color': 'darkblue'}, line_kws={'color': 'red'}, data=working_subset_5)
pyplot.xlabel('Crater Diameter (km)')
pyplot.ylabel('Crater Depth (km)')
pyplot.title('Relationship between Crater Diameter & Crater Depth for Lower Equator')
graph_4.set(xlim=(0, 120))
graph_4.set(ylim=(0, 4))
pyplot.xticks(numpy.arange(0, 120+20, 20))
pyplot.yticks(numpy.arange(0, 5+1, 1))
pyplot.tick_params(axis='both')
pyplot.show()


graph_5 = seaborn.lmplot(x='DIAM_CIRCLE_IMAGE', y='DEPTH_RIMFLOOR_TOPOG', fit_reg=True, scatter_kws={'color': 'darkblue'}, line_kws={'color': 'red'}, data=working_subset_6)
pyplot.xlabel('Crater Diameter (km)')
pyplot.ylabel('Crater Depth (km)')
pyplot.title('Relationship between Crater Diameter & Crater Depth for South Pole')
graph_5.set(xlim=(0, 120))
graph_5.set(ylim=(0, 4))
pyplot.xticks(numpy.arange(0, 120+20, 20))
pyplot.yticks(numpy.arange(0, 5+1, 1))
pyplot.tick_params(axis='both')
pyplot.show()
