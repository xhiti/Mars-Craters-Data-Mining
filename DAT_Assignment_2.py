import numpy
import pandas
import seaborn
from scipy import stats
import matplotlib.pyplot as pyplot

# read from dataset
data = pandas.read_csv('dataset/marscrater_pds.csv', low_memory=False)

# bug fix for display formats to avoid run time errors
pandas.set_option('display.float_format', lambda x:'%f'%x)

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
    if row['LATITUDE_CIRCLE_IMAGE'] < 1:
        return
    elif row['LATITUDE_CIRCLE_IMAGE'] < -45:
        return 3
    else:
        return 2

working_subset_2['MARS_REGION'] = working_subset_2.apply(lambda row: MARS_REGION(row), axis=1)


def DEPTH_CATEGORY(row):
    if row['DEPTH_RIMFLOOR_TOPOG'] > 1:
        return 0
    else:
        return 1

working_subset_2['DEPTH_CATEGORY'] = working_subset_2.apply(lambda row: DEPTH_CATEGORY(row), axis=1)

# contingency table
contingency_table_1 = pandas.crosstab(working_subset_2['DEPTH_CATEGORY'], working_subset_2['MARS_REGION'])
print("# ==================== #")
print("# Contingency Table 1: #")
print("# ==================== #")
print()
print(contingency_table_1)
print()

# column percentages
col_sum = contingency_table_1.sum(axis=0)
col_percentage = contingency_table_1 / col_sum
print()
print("# ================== #")
print("# Column Percentage: #")
print("# ================== #")
print()
print(col_percentage)

# Chi-Square Test
chi_square_1 = stats.chi2_contingency(contingency_table_1)
print()
print("# ============= #")
print("# Chi-Square 1: #")
print("# ============= #")
print("Chi-Square value, p-value and expected counts")
print(chi_square_1)


# working_subset_2['MARS_REGION'] = working_subset_2['MARS_REGION'].astype('category')
working_subset_2['DEPTH_CATEGORY'] = pandas.to_numeric(working_subset_2['DEPTH_CATEGORY'], errors='coerce')


# graph
graph_1 = seaborn.catplot(x='MARS_REGION', y='DEPTH_CATEGORY', data=working_subset_2, kind='bar')
pyplot.xlabel("Region of Mars")
pyplot.ylabel("Proportion of deep craters")
pyplot.title("Percentage")
pyplot.show()


# Post-Hoc Chi-Square test for each category
recode_1 = {
    1: 1,
    2: 2
}

working_subset_2['COMPARISON_1_VS_2'] = working_subset_2['MARS_REGION'].map(recode_1)

contingency_table_2 = pandas.crosstab(working_subset_2['DEPTH_CATEGORY'], working_subset_2['COMPARISON_1_VS_2'])
print()
print()
print("# ==================== #")
print("# Contingency Table 2: #")
print("# ==================== #")
print()
print(contingency_table_2)
print()

# column percentages
col_sum_2 = contingency_table_2.sum(axis=0)
col_percentage_2 = contingency_table_2 / col_sum_2
print()
print("# =================== #")
print("# Column Percentage 2: #")
print("# =================== #")
print()
print(col_percentage_2)

# Chi-Square Test
chi_square_2 = stats.chi2_contingency(contingency_table_2)
print()
print("# ============= #")
print("# Chi-Square 2: #")
print("# ============= #")
print("Chi-Square value, p-value and expected counts")
print(chi_square_2)


recode_2 = {
    1: 1,
    3: 3
}

working_subset_2['COMPARISON_1_VS_3'] = working_subset_2['MARS_REGION'].map(recode_2)

contingency_table_3 = pandas.crosstab(working_subset_2['DEPTH_CATEGORY'], working_subset_2['COMPARISON_1_VS_3'])
print()
print()
print("# ==================== #")
print("# Contingency Table 3: #")
print("# ==================== #")
print()
print(contingency_table_3)
print()

# column percentages
col_sum_3 = contingency_table_3.sum(axis=0)
col_percentage_3 = contingency_table_3 / col_sum_3
print()
print("# ==================== #")
print("# Column Percentage 3: #")
print("# ==================== #")
print()
print(col_percentage_3)

# Chi-Square Test
chi_square_3 = stats.chi2_contingency(contingency_table_3)
print()
print("# ============= #")
print("# Chi-Square 3: #")
print("# ============= #")
print("Chi-Square value, p-value and expected counts")
print(chi_square_3)


recode_3 = {
    2: 2,
    3: 3
}

working_subset_2['COMPARISON_2_VS_3'] = working_subset_2['MARS_REGION'].map(recode_3)

contingency_table_4 = pandas.crosstab(working_subset_2['DEPTH_CATEGORY'], working_subset_2['COMPARISON_2_VS_3'])
print("# ==================== #")
print("# Contingency Table 4: #")
print("# ==================== #")
print()
print(contingency_table_4)
print()

# column percentages
col_sum_4 = contingency_table_4.sum(axis=0)
col_percentage_4 = contingency_table_4 / col_sum_4
print()
print("# ==================== #")
print("# Column Percentage 4: #")
print("# ==================== #")
print()
print(col_percentage_4)

# Chi-Square Test
chi_square_4 = stats.chi2_contingency(contingency_table_4)
print()
print("# ============= #")
print("# Chi-Square 4: #")
print("# ============= #")
print("Chi-Square value, p-value and expected counts")
print(chi_square_4)
