"""
Script for plotting new cases vs. total cases.
"""


import matplotlib.pyplot as plt
import pandas as pd
import os


CURRENT_DIRECTORY = os.path.dirname(__file__)


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


# script execution
countries = input('Enter country 3-letter codes separated by ", ": ').split(', ')
data_type = input('Cases or deaths? ')
period = int(input('Averaging period (in days): '))


for index in range(len(countries)):
    total_storage_file = os.path.join(CURRENT_DIRECTORY, '../../data/total_'+data_type+'/'+countries[index]+'.csv')
    total_dataframe = pd.read_csv(total_storage_file)
    x = list(total_dataframe['total_'+data_type])[period:]

    daily_storage_file = os.path.join(CURRENT_DIRECTORY, '../../data/daily_'+data_type+'/'+countries[index]+'.csv')
    daily_dataframe = pd.read_csv(daily_storage_file)
    y = get_averages(list(daily_dataframe['daily_'+data_type]), period)

    plot = plt.loglog(x, y, label=countries[index], linewidth=2)

plt.xlabel('Total '+data_type)

plt.ylabel('New ' + data_type)
plt.title('New '+data_type+' averaged over past '+str(period)+' days vs total '+data_type)
plt.legend()

plt.show()
