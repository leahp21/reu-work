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

def memgator_for_link(url):
    dict_of_links = {}

'''
collect memgator html
'''

def iterate_memgator(url):
    print("Getting memgator URIM's... may take a bit")
    docker_link = "docker container run -it --rm oduwsdl/memgator " + url + "> memgator_mementos.html"
    os.system(docker_link)
    # print(split_memento_links("memgator_mementos.html"))

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
        
            if "web.archive.org" in parsed_url:
                #look at year of memento and see if it matches the eligibility
                
                if (int(split_date[3]) < 2019):
                    valid_links["wayback"].append(parsed_url)
            else:
                if ('archive.md' in parsed_url) and int(split_date[3]) >= 2020:
                    valid_links["archive_today"].append(parsed_url)

    return valid_links

'''
sends memento links to scraper (for web.archive.org links) and 
'''
def send_to_scraper(memento_dict):
    # open scraper up and send the link to the scraper. put output in a json file
    i = 0
    k = 0


    for memento_type, memento_list in memento_dict.items():
        print(memento_type, memento_list)
        if memento_type == 'wayback':
            for wayback_mem_url in memento_dict['wayback']:
                process_wayback_mem(wayback_mem_url)
        else:
             # = {'follower_count':follower_count, 'hashtags_used': ",".join(hashtag_list), 'mentions': ','.join(mention_list)}
            archive_today_data = pd.DataFrame(columns=['Follower_count','Hashtags','Mentions'])

            for archive_today_url in memento_dict['archive_today']:
                archive_today_data = process_archive_mem(archive_today_url, archive_today_data)
            
        #process_single_memento(memento)
        #process single memento
        #take relevant information from memento
        #store it in a row?

        
    '''
    if len(memento_dict["wayback"] >= 1):
        memento_link = memento_dict.get("wayback")[0]

        scraper_command = "python3 instagram_memento_scrape.py --urim " + memento_link + "> scraper_output.json"
        os.system(scraper_command)

        file = open('scraper_output.json')
        json_content = json.load(file)
    else:
        if (len(memento_dict["archive_today"]) >= 1):
            scraper_command = "python3 archive_today_scraper.py --urim " + memento_link + "> scraper_output.json"
            os.system(scraper_command)
    '''

def process_wayback_mem(mem_link):
    # scraper_command = "python3 instagram_memento_scrape.py --urim " + mem_link + "> scraper_output.json"
    # os.system(scraper_command)

    # scraper_command = "python3 archive_today_scraper.py --urim " + memento_link + "> scraper_output.json"
    # os.system(scraper_command)
    print(' ')

def process_archive_mem(archive_today_link, data_chart):
    archive_today_link = "https://archive.ph/pENox"
     
    scraper_command = "python3 archive_today_scraper.py --urim " + archive_today_link + "> scraper_output.json"
    os.system(scraper_command)

    file = open('scraper_output.json')

    try: 
        json_content = json.load(file)
    except:
        print('error opening file (maybe file is empty)')
    
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
        print('matched')
        hashtag_list.extend(re.findall('#\w+',json_content['bio']))
        
    elif len(re.findall('@[\w.]+',str(json_content['bio']))) != None:
        mention_list.extend(re.findall('@[\w.]+',str(json_content['bio'])))

    follower_count = json_content['follower_count'].split(' ')[0]

    # extracting follower_count
    if('m' in follower_count) or ('M' in follower_count):
        follower_count = int(float(re.match('([^>]+)[A-Za-z]',follower_count).group(1)) * 1000000)
    elif('k' in follower_count) or ('K' in follower_count):
        follower_count = int(float(re.match('([^>]+)[A-Za-z]',follower_count).group(1)) * 1000)
    else:
        follower_count = int(follower_count)

    memento_row = {'Follower_count':follower_count, 'Hashtags': ",".join(hashtag_list), 'Mentions': ','.join(mention_list)}
    data_chart.append(memento_row)

    return data_chart

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()

    iterate_memgator(args.url)
    memento_dict = split_memento_links("memgator_mementos.html")
    #print(memento_dict)
    send_to_scraper(memento_dict)