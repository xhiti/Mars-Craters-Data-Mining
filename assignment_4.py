# import libraries
import pandas
import numpy
import seaborn
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import openpyxl

# set PANDAS to show all columns in DataFrame
pandas.set_option('display.max_columns', None)
# set PANDAS to show all rows in DataFrame
pandas.set_option('display.max_rows', None)

# bug fix for display formats to avoid run time errors
pandas.set_option('display.float_format', lambda x:'%f'%x)

data = pandas.read_csv('dataset/marscrater_pds.csv', low_memory=False)

# number of observations (rows)
print('Number of records: ' + str(len(data)))
# number of variables (columns)
print('Number of variables: ' + str(len(data.columns)))

# checking the format of your variables
print('Data type for varibale DIAM_CIRCLE_IMAGE :' + str(data['DIAM_CIRCLE_IMAGE'].dtype))

# setting variables we will be working with to numeric
data['LATITUDE_CIRCLE_IMAGE'] = pandas.to_numeric(data['LATITUDE_CIRCLE_IMAGE'])
data['LONGITUDE_CIRCLE_IMAGE'] = pandas.to_numeric(data['LONGITUDE_CIRCLE_IMAGE'])
data['DIAM_CIRCLE_IMAGE'] = pandas.to_numeric(data['DIAM_CIRCLE_IMAGE'])
data['DEPTH_RIMFLOOR_TOPOG'] = pandas.to_numeric(data['DEPTH_RIMFLOOR_TOPOG'])
data['NUMBER_LAYERS'] = pandas.to_numeric(data['NUMBER_LAYERS'])

# subset data with craters with diameter between 50 and 80 kms
subset_1 = data[(data['DIAM_CIRCLE_IMAGE'] >= 50) & (data['DIAM_CIRCLE_IMAGE'] <= 80)]

# make a copy of subsetted data
subset_2 = subset_1.copy()

# recode missing values to python missing (NaN)
subset_2['NUMBER_LAYERS'] = subset_2['NUMBER_LAYERS'].replace(4, numpy.nan)

subset_2["NUMBER_LAYERS"] = subset_2["NUMBER_LAYERS"].astype('category')

seaborn.countplot(x="NUMBER_LAYERS", data=subset_2)
plt.xlabel('Number of lawyers for craters')
plt.title('Number of lawyers for craters with diameter between 50 an 80 kms')
plt.show()

# univariate histogram for quantitative variable:
seaborn.displot(subset_2["DIAM_CIRCLE_IMAGE"].dropna(), kde=False)
plt.xlabel('Number of Dimater of Craters')
plt.title('Estimated Number of Craters Diameter')
plt.show()

seaborn.catplot(x="DIAM_CIRCLE_IMAGE", y="NUMBER_LAYERS", data=subset_2, kind="bar", ci=None)
plt.xlabel('Diamter length (kms)')
plt.ylabel('Number of Lawyers')
plt.show()

scat1 = seaborn.regplot(x="DIAM_CIRCLE_IMAGE", y="NUMBER_LAYERS", fit_reg=False, data=subset_2)
plt.xlabel('UrbanDIAM_CIRCLE_IMAGE')
plt.ylabel('NUMBER_LAYERS')
plt.title('Relationship between two variables')

print('================================================')
print('Counts for original DIAM_CIRCLE_IMAGE Variable: ')
print('================================================')
count_1 = subset_2['DIAM_CIRCLE_IMAGE'].value_counts(sort=False, dropna=False)
print(count_1)
print()


# working more with the assignment 4
data['NUMBER_LAYERS'] = pandas.to_numeric(data['NUMBER_LAYERS'], errors='coerce')
data['DIAM_CIRCLE_IMAGE'] = pandas.to_numeric(data['DIAM_CIRCLE_IMAGE'], errors='coerce')
data['DEPTH_RIMFLOOR_TOPOG'] = pandas.to_numeric(data['DEPTH_RIMFLOOR_TOPOG'], errors='coerce')
data['LONGITUDE_CIRCLE_IMAGE'] = pandas.to_numeric(data['LONGITUDE_CIRCLE_IMAGE'], errors='coerce')
data['LATITUDE_CIRCLE_IMAGE'] = pandas.to_numeric(data['LATITUDE_CIRCLE_IMAGE'], errors='coerce')

# creating new subset
working_subset = data[
    (data['DEPTH_RIMFLOOR_TOPOG'] > 0) & (data['DEPTH_RIMFLOOR_TOPOG'] <= 3)
    & (data['DIAM_CIRCLE_IMAGE'] > 0) & (data['DIAM_CIRCLE_IMAGE'] <= 100)
]

graph_2 = seaborn.jointplot(
    x='LONGITUDE_CIRCLE_IMAGE', y='LATITUDE_CIRCLE_IMAGE', data=working_subset, kind='reg', color='#774499', dropna=True,
    height=13, space=0.3, ratio=4, xlim=(-180, 180), ylim=(-90, 90), fit_reg=False, marginal_kws={'color': '#ff0000'}
)
plt.setp(graph_2.ax_marg_y.patches, color='#0000ff')
plt.rc('legend')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Craters Location Working Dataset')
plt.tick_params(axis='both')
graph_2.ax_joint.xaxis.set_major_locator(ticker.MultipleLocator(90))
graph_2.ax_joint.yaxis.set_major_locator(ticker.MultipleLocator(45))
plt.show()
graph_2.savefig('output_location_working_dataset.png')


# frequency distribution for variable DEPTH_GROUP
depth = [0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0]
depth_labels = ['0 - 0.3', '0.3 - 0.6', '0.6 - 0.9', '0.9 - 1.2', '1.2 - 1.5', '1.5 - 1.8', '1.8 - 2.1', '2.1 - 2.4', '2.4 - 2.7', '2.7 - 3.0']
working_subset['DEPTH_GROUP'] = pandas.cut(working_subset.DEPTH_RIMFLOOR_TOPOG, bins=depth, labels=depth_labels, right=True)

print()
print('=========================================')
print('Value counts for varaible - DEPTH_GROUP: ')
print('=========================================')
count_depth_group = working_subset['DEPTH_GROUP'].value_counts(sort=False)
print(count_depth_group)
print()

# Percentages for DEPTH_GROUP Variable
print()
print('========================================')
print('Percentages for varaible - DEPTH_GROUP: ')
print('========================================')
percentages_depth_group = working_subset['DEPTH_GROUP'].value_counts(sort=False, normalize=True)
print(percentages_depth_group)
print()

print()
print('=========')
print('Results: ')
print('=========')
data_frame_1 = pandas.DataFrame(numpy.array(count_depth_group), index=count_depth_group.index.values, columns=['Frequency'])
data_frame_2 = pandas.DataFrame(numpy.array(percentages_depth_group * 100), index=percentages_depth_group.index.values, columns=['Percentage'])
output_depth_group = pandas.concat([data_frame_1, data_frame_2], axis=1)

output_depth_group['Frequency'] = output_depth_group.Frequency.cumsum()
output_depth_group['Percentage'] = output_depth_group.Percentage.cumsum()

output_depth_group.index.name = 'DEPTH_GROUP'
print(output_depth_group)
print()

working_subset['DEPTH_GROUP'] = working_subset['DEPTH_GROUP'].astype('category')

graph_3 = seaborn.countplot(
    x='DEPTH_GROUP', data=working_subset, saturation=1, palette='Set1'
)
plt.xlabel('DEPTH_GROUP (km)')
plt.ylabel('COUNT')
plt.title('Graph for Crater Depth')
plt.tick_params(axis='both')
plt.xticks(rotation=75)
plt.show()



# frequency distribution for variable DIAMETER_GROUP
diameter = [i for i in range(0, 105, 5)]
diameter_labels = ['{0} - {1}'.format(i, i+5) for i in range(0, 100, 5)]
working_subset['DIAMETER_GROUP'] = pandas.cut(working_subset.DIAM_CIRCLE_IMAGE, bins=diameter, labels=diameter_labels, right=True)

print()
print('============================================')
print('Value counts for varaible - DIAMETER_GROUP: ')
print('============================================')
count_diameter_group = working_subset['DIAMETER_GROUP'].value_counts(sort=False)
print(count_diameter_group)
print()

# Percentages for DIAMETER_GROUP Variable
print()
print('===========================================')
print('Percentages for varaible - DIAMETER_GROUP: ')
print('===========================================')
percentages_diameter_group = working_subset['DIAMETER_GROUP'].value_counts(sort=False, normalize=True)
print(percentages_diameter_group)
print()

print()
print('=========')
print('Results: ')
print('=========')
data_frame_3 = pandas.DataFrame(numpy.array(count_diameter_group), index=count_diameter_group.index.values, columns=['Frequency'])
data_frame_4 = pandas.DataFrame(numpy.array(percentages_diameter_group * 100), index=percentages_diameter_group.index.values, columns=['Percentage'])
output_diameter_group = pandas.concat([data_frame_3, data_frame_4], axis=1)

output_diameter_group['Frequency'] = output_diameter_group.Frequency.cumsum()
output_diameter_group['Percentage'] = output_diameter_group.Percentage.cumsum()

output_diameter_group.index.name = 'DIAMETER_GROUP'
print(output_diameter_group)
print()

working_subset['DIAMETER_GROUP'] = working_subset['DIAMETER_GROUP'].astype('category')

graph_4 = seaborn.countplot(
    x='DIAMETER_GROUP', data=working_subset, saturation=1, palette='Set1'
)
plt.xlabel('DIAMETER_GROUP (km)')
plt.ylabel('COUNT')
plt.title('Graph for Crater Diameter')
plt.tick_params(axis='both')
plt.xticks(rotation=75)
plt.show()



# frequency distribution for variable LATITUDE_GROUP
latitude = [i for i in range(-90, 105, 15)]
latitude_labels = ['{0} - {1}'.format(i, i+15) for i in range(-90, 90, 15)]
working_subset['LATITUDE_GROUP'] = pandas.cut(working_subset.LATITUDE_CIRCLE_IMAGE, bins=latitude, labels=latitude_labels, right=True)

print()
print('============================================')
print('Value counts for varaible - LATITUDE_GROUP: ')
print('============================================')
count_latitude_group = working_subset['LATITUDE_GROUP'].value_counts(sort=False)
print(count_latitude_group)
print()

# Percentages for LATITUDE_GROUP Variable
print()
print('===========================================')
print('Percentages for varaible - LATITUDE_GROUP: ')
print('===========================================')
percentages_latitude_group = working_subset['LATITUDE_GROUP'].value_counts(sort=False, normalize=True)
print(percentages_latitude_group)
print()

print()
print('=========')
print('Results: ')
print('=========')
data_frame_5 = pandas.DataFrame(numpy.array(count_latitude_group), index=count_latitude_group.index.values, columns=['Frequency'])
data_frame_6 = pandas.DataFrame(numpy.array(percentages_latitude_group * 100), index=percentages_latitude_group.index.values, columns=['Percentage'])
output_latitude_group = pandas.concat([data_frame_5, data_frame_6], axis=1)

output_latitude_group['Frequency'] = output_latitude_group.Frequency.cumsum()
output_latitude_group['Percentage'] = output_latitude_group.Percentage.cumsum()

output_latitude_group.index.name = 'LATITUDE_GROUP'
print(output_latitude_group)
print()


working_subset['LATITUDE_GROUP'] = working_subset['LATITUDE_GROUP'].astype('category')

graph_5 = seaborn.countplot(
    x='LATITUDE_GROUP', data=working_subset, saturation=1, palette='Set1'
)
plt.xlabel('LATITUDE_GROUP')
plt.ylabel('COUNT')
plt.title('Graph for Crater Latitude')
plt.tick_params(axis='both')
plt.xticks(rotation=75)
plt.show()


# Does we have a relationship betwwen DIAM_CIRCLE_IMAGE and DEPTH_RIMFLOOR_TOPOG?
graph_6 = seaborn.lmplot(
    x='DIAM_CIRCLE_IMAGE', y='DEPTH_RIMFLOOR_TOPOG', data=working_subset, size=9, fit_reg=False
)
plt.xlabel('CRATER DIAMETER (km)')
plt.ylabel('CRATER DEPTH (km)')
plt.title('Relationship betwwen DIAM_CIRCLE_IMAGE and DEPTH_RIMFLOOR_TOPOG')
graph_6.set(xlim=(0, 120))
graph_6.set(ylim=(0, 4))
plt.xticks(numpy.arange(0, 120+20, 20))
plt.yticks(numpy.arange(0, 4+1, 1))
plt.tick_params(axis='both')
plt.show()