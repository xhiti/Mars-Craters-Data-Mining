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

# choosen subset to work with
working_subset_1 = data[
    (data['NUMBER_LAYERS'] > 0) & (data['DIAM_CIRCLE_IMAGE'] > 0) & (data['DIAM_CIRCLE_IMAGE'] <= 100)
    & (data['DEPTH_RIMFLOOR_TOPOG'] > 0) & (data['DEPTH_RIMFLOOR_TOPOG'] <= 3)
]

working_subset_2 = working_subset_1.copy()


# calculate Pearson coefficient
print('Association between CRATER DIAMETER and CRATER DEPTH')
print(stats.pearsonr(working_subset_2['DIAM_CIRCLE_IMAGE'], working_subset_2['DEPTH_RIMFLOOR_TOPOG']))
print()
print()

# calculate regresion parameters
slope, intercept, r_value, p_value, standart_error = stats.linregress(working_subset_2['DIAM_CIRCLE_IMAGE'], working_subset_2['DEPTH_RIMFLOOR_TOPOG'])
print("Slope: " + str(slope))
print("Intercept: " + str(intercept))
print("P-value: " + str(p_value))
print("R-value: " + str(r_value))
print()
print()

# calculate standart error
X = stats_models_api.add_constant(working_subset_2['DIAM_CIRCLE_IMAGE'])
model = stats_models_api.OLS(working_subset_2['DEPTH_RIMFLOOR_TOPOG'], X)
results = model.fit()
calculate_standart_error = numpy.sqrt(results.mse_resid)
print("r = " + str(r_value))
print("power(r, 2) = " + str(r_value ** 2))
print("P-value = " + str(p_value))
print("Standart Deviation = " + str(calculate_standart_error))
print()
print()

# create graph
graph_1 = seaborn.lmplot(x='DIAM_CIRCLE_IMAGE', y='DEPTH_RIMFLOOR_TOPOG', fit_reg=True, line_kws={'color': 'red'}, data=working_subset_2)
pyplot.xlabel('Crater Diameter (km)')
pyplot.ylabel('Crater Depth (km)')
pyplot.title('Relationship between Crater Diameter & Crater Depth')
graph_1.set(xlim=(0, 120))
graph_1.set(ylim=(0, 4))
pyplot.xticks(numpy.arange(0, 120+20, 20))
pyplot.yticks(numpy.arange(0, 4+1, 1))
pyplot.tick_params(axis='both')
pyplot.text(20, 3.5, "y = %.5f x + %.5f" % (slope, intercept), color='red')
pyplot.text(20, 3.3, "power(r, 2) = %.5f" % (r_value ** 2), color='red')
pyplot.show()
