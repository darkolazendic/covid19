"""
Script for plotting a simple cases vs. time chart.
"""


import matplotlib.pyplot as plt
import pandas as pd
import os


CURRENT_DIRECTORY = os.path.dirname(__file__)


countries = input('Enter country 3-letter codes separated by ", ": ').split(', ')
data_type = input('Plot types (total or daily): ')


for index in range(len(countries)):
    storage_file = os.path.join(CURRENT_DIRECTORY, '../../data/'+data_type+'_cases'+'/'+countries[index]+'.csv')
    dataframe = pd.read_csv(storage_file)

    x = list(dataframe['date'])
    y = list(dataframe[data_type+'_cases'])

    plot = plt.plot(x, y, label=countries[index])

ax = plt.gca()

plt.xlabel('date')
plt.xticks(rotation=90)
[l.set_visible(False) for (i, l) in enumerate(ax.xaxis.get_ticklabels()) if i % 3 != 0]

plt.ylabel(data_type.capitalize()+' COVID-19 cases')
plt.title(data_type.capitalize()+' COVID-19 cases')
plt.legend()

plt.show()
