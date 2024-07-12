import pandas as pd
import argparse
import re
from datetime import datetime
import numpy as np

def generate_follower_chart(csv_file):
    csv_list = []

    with open(csv_file,'r') as csv_files:
        for line in csv_files:
            print(line.split(',')[0])
            csv_list.append(line.split(',')[0])

    follower_df = pd.DataFrame()
    
    for csv in csv_list:
        account_name = re.search('([^\/]+)\.csv$', csv).group(1)

        memento_count = 0
        max_follower_count = 0
        min_follower_count = 0

        min_max_follower_growth = 0
        avg_growth = 0

        prev_index = 0
        curr_index = 1

        new_df = pd.DataFrame()
        

        df = pd.read_csv(csv)
        df = df.drop_duplicates(subset=['Follower_count', 'Comment_count', 'Like_count','Hashtags', 'Hashtag_count', 'Mentions', 'Mention_count'], keep='first')
        df = df.dropna(thresh=2)

        if len(df) == 0:
            follower_df = follower_df.append({"Account Name" : account_name, "Maximum Followers": np.nan, "Max-min Follower growth": np.nan, "Minimum Followers": np.nan
                                              , "Number of mementos": np.nan, "Memento time covered": np.nan, "Memento date range": np.nan},
                                          ignore_index=True)
        else:
            for index, row in df.iterrows():
                if pd.notna(row['Follower_count']):
                    memento_count += 1
                    new_df = new_df.append({'Date': row['Date'], 'Follower_count': row['Follower_count']}, ignore_index=True)

                    if int(row['Follower_count']) > max_follower_count:
                        max_follower_count = int(row['Follower_count'])
                    
                    if (curr_index < len(df)):
                        avg_growth += (df.iloc[curr_index]['Follower_count'] - df.iloc[prev_index]['Follower_count'])/ df.iloc[prev_index]['Follower_count']

                    prev_index += 1
                    curr_index += 1 
            
            # new_df.set_index('Date')

            if memento_count >= 2:
                first_follower_count = new_df.iloc[0]['Follower_count']
                last_follower_count = new_df.iloc[-1]['Follower_count']

                min_follower_count = first_follower_count

                min_max_follower_growth = ((last_follower_count - first_follower_count)/first_follower_count) * 100

                start_date = datetime.strptime(new_df.iloc[0]['Date'], "%Y-%m-%d %H:%M:%S")
                last_date = datetime.strptime(new_df.iloc[-1]['Date'], "%Y-%m-%d %H:%M:%S")

                date_range = last_date - start_date

                date_range_str = new_df.iloc[0]['Date'], new_df.iloc[-1]['Date']
                minutes = 0
                left_over = 0

                if date_range.seconds > 60:
                    hours = date_range.seconds // 3660
                    minutes = (date_range.seconds % 3600) //  60
                    left_over = (date_range.seconds % 3600) % 60

                date_string = str(date_range.days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes, " + str(left_over) + " seconds"

                avg_growth /= (memento_count - 1)

                avg_growth *= 100
            
            else:
                avg_growth = 0
                min_follower_count = max_follower_count
                date_string = np.nan
                date_range_str = new_df.iloc[0]['Date']

            
            follower_df = follower_df.append({"Account Name" : account_name, "Minimum Followers": min_follower_count, "Maximum Followers": int(max_follower_count), "Max-min Follower growth (%)": min_max_follower_growth,
                                               "Number of mementos": int(memento_count), "Memento time covered": date_string, "Memento date range": date_range_str},
                                            ignore_index=True)
        
    pd.set_option('display.max_columns', None)
    print(follower_df)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("csv_text_file")
    args = parser.parse_args()

    generate_follower_chart(args.csv_text_file)