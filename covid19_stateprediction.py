import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import mpld3
import json

data = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv', 
                    header = 0, 
                    error_bad_lines=False, 
                    skip_blank_lines=True)

#Add ability to view multiple graphs and compare them.

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

#Builds the dataframe that will be visualized
def build_dataframe(input, state):
    frame = extract_rows(input, state)
    frame = convert_date(frame)
    cases, deaths = add_daily_count(frame)
    frame['daily cases'] = cases
    frame['daily deaths'] = deaths
    return frame

#Takes a list of tickers and returns a revised list
def reduce_tickers(ticker_list, reduce):
    ticker_list = ticker_list[0]
    interval = int(len(ticker_list)/reduce)
    back_interv = interval
    tick_list = [0]
    while interval < len(ticker_list):
        tick_list.append(interval)
        interval = interval + back_interv
    return tick_list

#Builds and displays a plot
def visualize_dataframe(input, state):
    select = build_dataframe(input, state)
    df = pd.DataFrame(select, columns = select.columns.values)
    fig,ax = plt.subplots()
    ax.plot(df['date'], df['daily cases'], color="red", marker="o")
    ax.set_xlabel("Date",fontsize=1100)
    ax.set_ylabel("Cases Per Day",color="red",fontsize=14)
    ax2 = ax.twinx()
    ax2.plot(df['date'], df['daily deaths'],color="blue",marker="o")
    ax2.set_ylabel("Deaths Per Day",color="blue",fontsize=14)
    header = 'Daily COVID-19 Cases and Deaths for {}'.format(state)
    plt.title(header)
    tick_list = reduce_tickers(plt.xticks(),8)
    plt.xticks(ticks=tick_list)
    plt.show()


if __name__=="__main__":
    print('==COVID-19 Per-State Daily Case and Death Count==')
    print('Which state would you like to view data for?')
    print("NOTE: Please enter the state's full name, such as 'New York' or 'Nevada'.")
    state = input('>')
    visualize_dataframe(data, state)