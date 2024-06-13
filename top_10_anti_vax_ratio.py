import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np

def bar_chart_mem_avail(data_chart):
    
    plt.figure()
    plt.barh(y=data_chart['account name'],width=data_chart['loadable archive_is mementos between 2019-2023'])
    plt.barh(y=data_chart['account name'],width=data_chart['wayback loadable mementos'])

    plt.legend(["archive.is", "Wayback Machine"])
    plt.title('Loadable Wayback Machine Mementos 2013-Mid 2019 and archive.is Mementos 2019-2023')
    plt.xlabel('Number of Loadable Mementos from Wayback Machine and archive.is')
    plt.ylabel('Instagram Account Name')
    plt.show()

def bar_chart_mem_ratio(data_chart):

    plt.figure()

    plt.barh(y=data_chart['account name'],width=((data_chart['loadable archive_is mementos between 2019-2023']/ data_chart['total number of mementos archive.is']) * 100))
    plt.barh(y=data_chart['account name'],width=((data_chart['wayback loadable mementos'] / data_chart['total number of wayback mementos between (2013 and mid 2019)']) * 100))

    plt.legend(["archive.is", "Wayback Machine"])
    plt.title('Ratio of Loadable Wayback Machine Mementos 2013-Mid 2019 and archive.is Mementos 2019-2023')
    plt.xlabel('Percent of Loadable Mementos from Wayback Machine and archive.is')
    plt.ylabel('Instagram Account Name')

    plt.show()

def bar_chart_archive_is(data_chart):

    plt.figure(figsize=(5,4))

    fig, ax = plt.subplots()

    boop = np.arange(len(data_chart))

    ax.barh(boop -0.2, data_chart['loadable archive_is mementos between 2019-2023'], 0.4)
    ax.barh(boop + 0.2, data_chart['total number of mementos archive.is'], 0.4)

    ax.set(yticks=boop, yticklabels=data_chart['account name'])

    plt.legend(["Number of Loadable Mementos", "Total Number of Mementos"])
    plt.title('Total Mementos and Scrapable Mementos from archive.is for Top 10 Anti-Vaxxers Between 2019-2023')
    plt.xlabel('Number of archive.is Mementos')
    plt.ylabel('Instagram Account Name')

    plt.show()

def bar_chart_wayback(data_chart):
    plt.figure(figsize=(5,4))

    fig, ax = plt.subplots()

    boop = np.arange(len(data_chart))

    ax.barh(boop -0.2, data_chart['wayback loadable mementos'], 0.4)
    ax.barh(boop + 0.2, data_chart['total number of wayback mementos between (2013 and mid 2019)'], 0.4)

    ax.set(yticks=boop, yticklabels=data_chart['account name'])

    plt.legend(["Number of Loadable Mementos", "Total Number of Mementos"])
    plt.title('Total Mementos and Scrapable Mementos from Wayback Machine for Top 10 Anti-Vaxxers Between 2013-Mid 2019')
    plt.xlabel('Number of Wayback Machine Mementos')
    plt.ylabel('Instagram Account Name')

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    args = parser.parse_args()

    account_data_df = df = pd.read_csv(args.csv_file)    

    bar_chart_mem_avail(account_data_df)
    bar_chart_mem_ratio(account_data_df)
    bar_chart_archive_is(account_data_df)
    bar_chart_wayback(account_data_df)
