import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np

def stacked_bar_chart_wayback(data_chart):
    plt.barh(data_chart['account name'],
             width=data_chart['wayback loadable mementos'],
             color='blue')
    plt.barh(data_chart['account name'],
             width=(data_chart[
                 'total number of wayback mementos between (2013 and mid 2019)']) -
             (data_chart['wayback loadable mementos']),
             left=data_chart['wayback loadable mementos'],
             color='orange')
    plt.xlabel('Number of Scrapable/Non-scrapable Mementos')
    plt.ylabel('Account Names')
    plt.legend(["Scrapable Mementos", "Non-scrapable Mementos"])
    plt.title(
        'Scrapable and Non-scrapable Wayback Machine Mementos for Health Authorities'
    )
    plt.tight_layout()
    plt.show()


def stacked_bar_chart_archive(data_chart):
    plt.barh(
        data_chart['account name'],
        width=data_chart['loadable archive_is mementos between 2019-2023'],
        color='blue')
    plt.barh(data_chart['account name'],
             width=data_chart['total number of mementos archive.is'] -
             data_chart['loadable archive_is mementos between 2019-2023'],
             left=data_chart['loadable archive_is mementos between 2019-2023'],
             color='orange')
    plt.xlabel('Number of Scrapable/Non-scrapable Mementos')
    plt.ylabel('Account Names')
    plt.legend(["Scrapable Mementos", "Non-scrapable Mementos"])
    plt.title(
        'Scrapable and Non-scrapable Archive.today Mementos for Health Authorities'
    )
    plt.tight_layout()
    plt.show()


def stacked_bar_chart_total(data_chart):

    plt.barh(data_chart['account name'],
             width=data_chart['Total Loadable Mementos'],
             color='b')
    plt.barh(data_chart['account name'],
             width=data_chart['Total Mementos'] -
             data_chart['Total Loadable Mementos'],
             left=data_chart['Total Loadable Mementos'],
             color='orange')

    plt.xlabel('Number of Scrapable/Non-scrapable Mementos')
    plt.ylabel('Account Names')
    plt.legend(["Scrapable Mementos", "Non-scrapable Mementos"])
    plt.title('Scrapable and Non-scrapable Mementos for Top 10 Anti-vaxxers')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    args = parser.parse_args()

    account_data_df = df = pd.read_csv(args.csv_file)

    '''
    bar_chart_mem_avail(account_data_df)
    bar_chart_mem_ratio(account_data_df)
    bar_chart_archive_is(account_data_df)
    bar_chart_wayback(account_data_df)
    '''
    stacked_bar_chart_wayback(account_data_df.sort_values('total number of wayback mementos between (2013 and mid 2019)', ascending=False))
    stacked_bar_chart_archive(account_data_df.sort_values('total number of mementos archive.is', ascending=False))

    stacked_bar_chart_total(account_data_df.sort_values('Total Mementos', ascending=False))
