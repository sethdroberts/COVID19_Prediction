import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

data = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv', 
                    header = 0, 
                    error_bad_lines=False, 
                    skip_blank_lines=True)

#Find a way to iterate through the list and just add it as a new list in the states list.

#List of all states, and that list contains a list of all states. 
# Won't be able to use for deep learning until I find a way to repopulate missing data in csv file.
state_data = []

#print(data)

#Takes a dataframe and returns two lists -- the daily case and daily death count
#WARNING: Only call in a dataframe for a specific state/county, or you will mess up data
def add_daily_count(input):
    cases_column = []
    deaths_column = []
    previous_case = 0
    previous_death = 0
    for index, row in input.iterrows():
        if len(cases_column) == 0:
            cases_column.append(int(row['cases']))
            deaths_column.append(int(row['deaths']))
            previous_case = int(row['cases'])
            previous_death = int(row['deaths'])
        else:
            daily_cases = int(row['cases']) - previous_case
            daily_deaths = int(row['deaths']) - previous_death
            cases_column.append(daily_cases)
            deaths_column.append(daily_deaths)
            previous_case = int(row['cases'])
            previous_death = int(row['deaths'])
    return cases_column, deaths_column
        
# print(add_daily_count(data))

#Takes a dataframe and returns all rows with a specified column value
def extract_rows(input, state):
    input = input.copy()
    select = input['state'] == state
    select = input[select]
    return select

#Converts dates in a dataframe from YYYY/MM/DD to MM/DD
def convert_date(input):
    input = input.copy()
    my_date = 0
    for index, row in input.iterrows():
        my_date = datetime.strptime(row['date'], "%Y-%m-%d")
        new_date = '{}/{}'.format(my_date.month, my_date.day)
        input.replace(row['date'], new_date, inplace = True)
    return input

def build_dataframe(input, state):
    frame = extract_rows(input, state)
    frame = convert_date(frame)
    cases, deaths = add_daily_count(frame)
    frame['daily cases'] = cases
    frame['daily deaths'] = deaths
    return frame

# print(build_dataframe(data, 'Michigan'))

def build_plot(input, state):
    select = build_dataframe(input, state)
    df = pd.DataFrame(select, columns = select.columns.values)
    df.plot(x ='date', y='daily deaths', kind = 'line')
    ax = df['daily deaths'].plot(secondary_y=True, color='k', marker='o')
    ax.set_ylabel('daily deaths')
    plt.show()

# build_plot(data, 'Michigan')
#Two options -- view cases/deaths for a state, or compare cases OR deaths betweens states
def visualize_dataframe(input, state):
    select = build_dataframe(input, state)
    df = pd.DataFrame(select, columns = select.columns.values)
    fig,ax = plt.subplots()
    ax.plot(df['date'], df['daily cases'], color="red", marker="o")
    every_nth = 4
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    ax.set_xlabel("Date",fontsize=14)
    ax.set_ylabel("Cases Per Day",color="red",fontsize=14)
    ax2 = ax.twinx()
    ax2.plot(df['date'], df['daily deaths'],color="blue",marker="o")
    ax2.set_ylabel("Deaths Per Day",color="blue",fontsize=14)
    header = 'Daily COVID-19 Cases and Deaths for {}'.format(state)
    plt.title(header)
    plt.show()

visualize_dataframe(data, 'Michigan')
