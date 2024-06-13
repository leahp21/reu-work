import matplotlib.pyplot as plt
import pandas as pd
import argparse

def process_hashtags(data_chart):
    # count hashtags for a given account 
    
    if data_chart.empty != True:
        data_chart.reset_index(inplace=True)

        if 'Date' in data_chart.columns:
            
            data_chart['Date'] = pd.to_datetime(data_chart['Date'])

            data_chart.set_index('Date', inplace=True)

            plt.figure()
            plt.plot(data_chart.index, data_chart['Follower_count'], marker='o', color='b')
            plt.plot(data_chart.index, data_chart['Hashtag_count'], marker='o', color='g')
            plt.legend('Count of hashtags per memento')
            plt.xlabel('Date')
            plt.ylabel('Number of hashtags')
            plt.title('Hashtag count vs Followers')
            plt.show()

            #top_three_hashtags(data_chart)
            unique_hashtag_count(data_chart)


def process_mentions(data_chart):
    mention_dict = {}

    # counts and displays mentions
    for index, row in data_chart.iterrows():
        mention_list = row['Mentions'].split(',')
        
        for i in range (0, len(mention_list)):
            account_mention = mention_list[i].lower()

            if (account_mention in mention_dict.keys()):
                mention_dict[account_mention] += 1
            else:
                mention_dict[account_mention] = 1
    
    account_mention_df = pd.DataFrame()

    for key, value in mention_dict.items():
        new_row = {"Mentions": key, "Mention_count": value}
        account_mention_df = account_mention_df.append(new_row, ignore_index=True)

    plt.figure()
    plt.barh(y=account_mention_df['Mentions'], width=account_mention_df['Mention_count'])
    plt.title('Account Mentions in Mementos Between ' + str(data_chart.index[0]) + ' and ' + str(data_chart.index[-1]))
    plt.xlabel('Frenquency of Account Mention')
    plt.ylabel('Account Mentions')
    plt.show()

def unique_hashtag_count(data_chart):
    hashtag_dict = {}

    # graph for counting hashtags over date range
    for index, row in data_chart.iterrows():
        if row['Hashtags'] != np.nan:
            hashtag_list = row['Hashtags'].split(',')
        
            for i in range (0, len(hashtag_list)):
                account_mention = hashtag_list[i].lower()

                if (account_mention in hashtag_dict.keys()):
                    hashtag_dict[account_mention] += 1
                else: 
                    hashtag_dict[account_mention] = 1
    
    account_hashtags_df = pd.DataFrame()

    for key, value in hashtag_dict.items():
        new_row = {"Hashtags": key, "Hashtag_count": value}
        account_hashtags_df = account_hashtags_df.append(new_row, ignore_index=True)

    if len(hashtag_dict) != 0:
        plt.figure()
        plt.barh(y=account_hashtags_df['Hashtags'], width=account_hashtags_df['Hashtag_count'])
        plt.title('Account Hashtag Usage in Mementos Between ' + str(data_chart.index[0]) + ' and ' + str(data_chart.index[-1]))
        plt.xlabel('Frequency of Hashtags')
        plt.ylabel('Hashtags')
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    args = parser.parse_args()

    account_data_df = df = pd.read_csv(args.csv_file)    

    process_hashtags(account_data_df)
    process_mentions(account_data_df)