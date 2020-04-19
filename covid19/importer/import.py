"""
Script for pulling JSON data and storing it locally. We are storing data per country, and only date and total cases
number or daily cases number are stored in a CSV file. Data is pulled from GitHub page
https://github.com/covid19-data/covid19-data/output. We are using ECDC data.
"""


import csv
import requests
import os


CURRENT_DIRECTORY = os.path.dirname(__file__)
SOURCE_URL = 'https://raw.githubusercontent.com/covid19-data/covid19-data/master/output/cntry_stat_ecdc_wp.json'


def write_to_csv(country_code, country_data, data_type):
    """
    Writes country cases data to local CSV file.
    :param country_code:
    :param country_data:
    :param data_type:
    :return:
    """

    storage_file = os.path.join(CURRENT_DIRECTORY, '../../data/'+data_type+'/' + country_code + '.csv')

    with open(storage_file, 'w', newline='') as csv_file:
        fieldnames = ['date', data_type]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for daily_data in country_data:
            writer.writerow({'date': daily_data[0], data_type: daily_data[1]})


def calculate_daily(country_data):
    """
    Calculates daily new cases/deaths data from total confirmed cases/deaths data.
    :param country_data:
    :return:
    """

    dates = []
    total = []
    daily = []

    for country_datum in country_data:
        dates.append(country_datum[0])
        total.append(country_datum[1])

    for index in range(len(dates)):
        previous = total[index-1] if index > 0 else 0
        daily.append([dates[index], total[index] - previous])

    return daily


# script execution
try:
    response = requests.get(SOURCE_URL).json()
except ValueError:
    exit('\nInvalid response returned by ' + SOURCE_URL + '. \n')
else:
    print(len(response))
    for data in response:
        # storing total cases and deaths data
        write_to_csv(data['country_code'], data['confirmed'], 'total_cases')
        write_to_csv(data['country_code'], data['deaths'], 'total_deaths')

        # calculating and storing daily new cases and deaths data
        write_to_csv(data['country_code'], calculate_daily(data['confirmed']), 'daily_cases')
        write_to_csv(data['country_code'], calculate_daily(data['deaths']), 'daily_deaths')

    print('\nTotal cases and deaths pulled and daily new cases and deaths calculated successfully.\n')
