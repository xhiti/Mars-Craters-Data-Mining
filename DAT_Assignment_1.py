import pandas
import numpy
import statsmodels.formula.api as stats_formula
import statsmodels.stats.multicomp as multicomp
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
print(model_1.summary())
print()


working_subset_3 = working_subset_2[['DEPTH_RIMFLOOR_TOPOG', 'MARS_REGION']].dropna()
print()
average_1 = working_subset_3.groupby('MARS_REGION').mean()
print("# ================================================== #")
print("# Mesatarja e thellesive te kratereve sipas grupeve: #")
print("# ================================================== #")
print(average_1)
print()

print()
standart_deviation_1 = working_subset_3.groupby('MARS_REGION').std()
print("# ========================================================== #")
print("# Devijimi standart i thellesive te kratereve sipas grupeve: #")
print("# ========================================================== #")
print(standart_deviation_1)
print()

# Post Hoc Test
multi_comparison_1 = multicomp.MultiComparison(
    working_subset_3['DEPTH_RIMFLOOR_TOPOG'],
    working_subset_3['MARS_REGION']
)
result_1 = multi_comparison_1.tukeyhsd()
print("# ================ #")
print("# Tukeyhsd Result: #")
print("# ================ #")
print(result_1.summary())
print()

# groups means visualisation
box_props = dict(linewidth=1.2)
mean_point_props = dict(marker='D', markeredgecolor='black', markerfacecolor='firebrick')
figure, ax = pyplot.subplots(figsize=(10, 12))

figure = working_subset_3.boxplot(
    'DEPTH_RIMFLOOR_TOPOG',
    'MARS_REGION',
    boxprops=box_props,
    meanprops=mean_point_props,
    meanline=False,
    showmeans=True,
    ax=ax,
    grid=False
)

pyplot.xlabel('MARS_REGION')
pyplot.ylabel('DEPTH_RIMFLOOR_TOPOG')
pyplot.title('Crater Depth BoxhPlot group by Mars Region', y=1.02)
pyplot.tick_params(axis='both')
pyplot.show()
ax.figure.savefig('output_DAT_assignment_1,png')
