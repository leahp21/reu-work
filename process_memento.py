'''
given a URL, call CDX API. Add memento links to a URL and 
'''

import requests
from bs4 import BeautifulSoup
import argparse
import re
import sys
import subprocess
import os
import json
import pandas as pd
from datetime import datetime
import time
import numpy as np

def memgator_for_link(url):
    dict_of_links = {}

'''
collect memgator html
'''

def iterate_memgator(url):
    print("Getting memgator URIM's... may take a bit")
    docker_link = "docker container run -it --rm oduwsdl/memgator " + url + "> memgator_mementos.html"
    os.system(docker_link)

'''
split memgator html to get valid dates and memento links
'''

def split_memento_links(filename):
    line_list = []
    valid_links = {}
    valid_links["wayback"] = []
    valid_links["archive_today"] = []

    with open(filename, 'r') as file:
        memento_lines = file.readlines()

    for line in memento_lines:
        line_list.append(line.strip().split(','))
    
    for link in line_list:
        # check if memento is in the line. If so, check if it is a wayback machine link or another link. If wayback link, check if it has a valid date and if it does, go to dictionary
        if "memento" in link[0]:
            split_line = link[0].split(';')
            memento_url = split_line[0]
            date = link[1]
            
            parsed_url = (re.search("<([^>]+)>", memento_url)).group(1)
            split_date = date.split(" ")

            day = split_date[1]
            month = split_date[2]
            year = split_date[3]
            time = split_date[4]

            date_string = f"{day} {month} {year} {time}"
            date_format = "%d %b %Y %H:%M:%S"

            date_obj = datetime.strptime(date_string, date_format)

            formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
        
            if "web.archive.org" in parsed_url:
                #look at year of memento and see if it matches the eligibility
                print(split_date)
                if (int(split_date[3]) < 2019) and (int(split_date[3]) >= 2013):
                    valid_links["wayback"].append([parsed_url,formatted_date])
            else:
                if ('archive.md' in parsed_url) and int(split_date[3]) >= 2020:
                    valid_links["archive_today"].append([parsed_url,formatted_date])

    return valid_links 

'''
sends memento links to scraper (for web.archive.org links) and 
'''
def send_to_scraper(memento_dict):
    # open scraper up and send the link to the scraper. put output in a json file
    i = 0
    k = 0
    archive_today_data = pd.DataFrame(columns=['Date','Follower_count','Hashtags','Hashtag_count','Mentions','Mention_count'])
    wayback_data = pd.DataFrame(columns=['Date','Follower_count',"Comment_count", 'Like_count','Hashtags','Hashtag_count','Mentions','Mention_count'])

    for memento_type, memento_list in memento_dict.items():
        #print(memento_type, memento_list)
        if memento_type == 'wayback':

            for wayback_mem_url in memento_dict['wayback']:
                wayback_data = process_wayback_mem(wayback_mem_url, wayback_data)
                time.sleep(10)

            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)

            wayback_data.set_index('Date',inplace=True)

        else:
             # = {'follower_count':follower_count, 'hashtags_used': ",".join(hashtag_list), 'mentions': ','.join(mention_list)}
            # archive_today_data = pd.DataFrame(columns=['Date','Follower_count','Hashtags','Mentions'])

            for archive_today_url in memento_dict['archive_today']:
                # print(k)
                archive_today_data = process_archive_mem(archive_today_url, archive_today_data)
                k += 1
            
            archive_today_data.set_index('Date', inplace = True)

        result = wayback_data.append(archive_today_data)
        print(result)


def process_wayback_mem(mem_link, data_chart):

    # test_link = "https://web.archive.org/web/20161117205615/https://www.instagram.com/army_of_jesus_/"

    scraper_command = "python3 instagram_memento_scrape.py --urim " + mem_link[0] + " > scraper_output.json"
    os.system(scraper_command)

    file = open('scraper_output.json')

    try: 
        json_content = json.load(file)
    except:
        print('error opening file (maybe file is empty)')
        memento_row = {'Date':mem_link[1],'Follower_count':np.nan, 'Hashtags': np.nan, 'Mentions': np.nan}
        data_chart = data_chart.append(memento_row, ignore_index=True)

        return data_chart
    
    hashtag_list = []
    mention_list = []
    follower_count = json_content['profileUser']['count']['followed_by']
    comment_count = 0
    like_count = 0

        # likes
        # comment count
        
    for post_detail in json_content['userMedia']:

        print(post_detail) 

        if len(re.findall('#\w+',str(post_detail['caption']['text']))) != 0:
            hashtag_list.extend(re.findall('#\w+',post_detail['caption']['text']))
        
        if len(re.findall('@[\w.]+',str(post_detail['caption']['text']))) != 0:
            mention_list.extend(re.findall('@[\w.]+',post_detail['caption']['text']))

        like_count += post_detail["likes"]['count']
        
        comment_count += post_detail['comments']['count']

    if len(re.findall('#\w+',json_content['profileUser']['bio'])) != 0:
        hashtag_list.extend(re.findall('#\w+',json_content['profileUser']['bio']))

    if len(re.findall('@[\w.]+',json_content['profileUser']['bio'])) != 0:
        mention_list.extend(re.findall('@[\w.]+',json_content['profileUser']['bio']))

    memento_row = {'Date':mem_link[1],'Follower_count':follower_count, 'Comment_count': comment_count, 'Like_count': like_count, 
                   'Hashtags': ",".join(hashtag_list), 'Hashtag_count': len(hashtag_list), 'Mentions': ','.join(mention_list), 'Mention_count': len(mention_list)}
    data_chart = data_chart.append(memento_row, ignore_index=True)

    file.close()

    return data_chart

def process_archive_mem(archive_today_link, data_chart):
     
    scraper_command = "python3 archive_today_scraper.py --urim " + archive_today_link[0] + " > scraper_output.json"
    os.system(scraper_command)

    file = open('scraper_output.json')

    try: 
        json_content = json.load(file)
    except:
        print('error opening file (maybe file is empty)')
        return data_chart
    
    hashtag_list = []
    mention_list = []

    for value in json_content['Posts'].values():

        if value['image-text'] != None:

            #matching hashtags and mentions in image text
            if len(re.findall('#\w+',value['image-text'])) != 0:
                hashtag_list.extend(re.findall('#\w+',value['image-text']))

            if len(re.findall('@[\w.]+',str(value['image-text']))) != 0:
                mention_list.extend(re.findall('@[\w.]+',value['image-text']))
    
    # matching hashtags and mentions in bio
    if len(re.findall('#\w+',json_content['bio'])) != 0:
        hashtag_list.extend(re.findall('#\w+',json_content['bio']))
        
    if len(re.findall('@[\w.]+',str(json_content['bio']))) != 0:
        mention_list.extend(re.findall('@[\w.]+',str(json_content['bio'])))

    follower_count = json_content['follower_count'].split(' ')[0]

    # extracting follower_count
    if('m' in follower_count) or ('M' in follower_count):
        follower_count = int(float(re.match('([^>]+)[A-Za-z]',follower_count).group(1)) * 1000000)
    elif('k' in follower_count) or ('K' in follower_count):
        follower_count = int(float(re.match('([^>]+)[A-Za-z]',follower_count).group(1)) * 1000)
    else:
        follower_count = int(follower_count)

    memento_row = {'Date':archive_today_link[1],'Follower_count':follower_count, 'Hashtags': ",".join(hashtag_list), 
                   'Hashtag_count': len(hashtag_list), 'Mentions': ','.join(mention_list), 'Mention_count':len(mention_list)}
    data_chart = data_chart.append(memento_row, ignore_index=True)

    return data_chart

def process_hashtags(data_chart):
    # count hashtags for a given account 

    hashtag_count 



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()

    iterate_memgator(args.url)
    memento_dict = split_memento_links("memgator_mementos.html")
    #print(memento_dict)
    send_to_scraper(memento_dict)