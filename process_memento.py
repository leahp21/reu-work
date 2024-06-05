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

def memgator_for_link(url):
    dict_of_links = {}
    
def iterate_memgator(url):
    print("Getting memgator URIM's... may take a bit")
    docker_link = "docker container run -it --rm oduwsdl/memgator " + url + "> memgator_mementos.html"
    os.system(docker_link)
    # print(split_memento_links("memgator_mementos.html"))

def split_memento_links(filename):
    line_list = []
    valid_links = {}
    valid_links["wayback"] = []
    valid_links["other_archive"] = []

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
        
            if "web.archive.org" in parsed_url:
                #look at year of memento and see if it matches the eligibility
                split_date = date.split(" ")
                if (int(split_date[3]) < 2019):
                    valid_links["wayback"].append(parsed_url)
            else:
                valid_links["other_archive"].append(parsed_url)

    return valid_links
    
def send_to_scraper(memento_dict):
    # open scraper up and send the link to the scraper. put output in a json file

    memento_link = memento_dict.get("wayback")[0]

    scraper_command = "python3 instagram_memento_scrape.py --urim " + memento_link + "> scraper_output.json"
    os.system(scraper_command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()

    iterate_memgator(args.url)
    memento_dict = split_memento_links("memgator_mementos.html")
    print(memento_dict)
    # send_to_scraper(memento_dict)