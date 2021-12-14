import pandas as pd
import numpy as np
import statsmodels.formula.api as stats_formula
import statsmodels.stats.multicomp as multicomp
import matplotlib.pyplot as pyplot

# read from dataset
data = pd.read_csv('dataset/marscrater_pds.csv', low_memory=False)

# bug fix for display formats to avoid run time errors
pd.set_option('display.float_format', lambda x:'%f'%x)

# setting variables to numeric
data['LATITUDE_CIRCLE_IMAGE'] = pandas.to_numeric(data['LATITUDE_CIRCLE_IMAGE'], errors='coerce')
data['DEPTH_RIMFLOOR_TOPOG'] = pandas.to_numeric(data['DEPTH_RIMFLOOR_TOPOG'], errors='coerce')
data['NUMBER_LAYERS'] = pandas.to_numeric(data['NUMBER_LAYERS'], errors='coerce')

# choosen subset to work with
working_subset_1 = data[
    (data['NUMBER_LAYERS'] > 0) & (data['DIAM_CIRCLE_IMAGE'] > 0) & (data['DIAM_CIRCLE_IMAGE'] <= 100)
    & (data['DEPTH_RIMFLOOR_TOPOG'] > 0) & (data['DEPTH_RIMFLOOR_TOPOG'] <= 3)
]

working_subset_2 = working_subset_1.copy()


def MARS_REGION(row):
    if row['LATITUDE_CIRCLE_IMAGE'] > 45:
        return 1
    elif row['LATITUDE_CIRCLE_IMAGE'] < -45:
        return 3
    else:
        return 2


working_subset_2['MARS_REGION'] = working_subset_2.apply(lambda row: MARS_REGION(row), axis=1)


# calculating dhe F-statistic and p-value
model_1 = stats_formula.ols(
    formula='DEPTH_RIMFLOOR_TOPOG ~ C(MARS_REGION)',
    data=working_subset_2
).fit()
print("# ==================== #")
print("# Summary for Model 1: #")
print("# ==================== #")
print()

