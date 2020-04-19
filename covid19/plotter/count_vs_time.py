"""
Script for plotting a simple cases vs. time chart.
"""


import matplotlib.pyplot as plt
import pandas as pd
import os


CURRENT_DIRECTORY = os.path.dirname(__file__)


countries = input('Enter country 3-letter codes separated by ", ": ').split(', ')
data_type = input('Cases or deaths? ')
time_frame = input('Plot types (total or daily): ')

period = 1
if time_frame == 'daily':
    period = int(input('Averaging period (in days): '))


def get_averages(data, averaging_period):
    """
    Returns list of values averaged over averaging_period.
    :param data:
    :param averaging_period:
    :return:
    """

    averages = []

    for i in range(averaging_period, len(data)):
        averages.append(sum(data[i-averaging_period:i]) / averaging_period)

    return averages


for index in range(len(countries)):
    storage_file = os.path.join(CURRENT_DIRECTORY, '../../data/'+time_frame+'_'+data_type+'/'+countries[index]+'.csv')
    dataframe = pd.read_csv(storage_file)

    x = list(dataframe['date'])[period:]
    y = get_averages(list(dataframe[time_frame+'_'+data_type]), period)

    plot = plt.plot(x, y, label=countries[index], linewidth=2)

ax = plt.gca()

plt.xlabel('date')
plt.xticks(rotation=90)
[l.set_visible(False) for (i, l) in enumerate(ax.xaxis.get_ticklabels()) if i % 3 != 0]

plt.ylabel(time_frame.capitalize()+' COVID-19 '+data_type)
plt.title(time_frame.capitalize()+' COVID-19 '+data_type+
          (' averaged over past '+str(period)+' days' if time_frame == 'daily' else ''))
plt.legend()

plt.show()
