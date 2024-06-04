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

def memgator_for_link(url):
    dict_of_links = {}

    
def iterate_memgator(url):
    docker_link = "docker container run -it --rm oduwsdl/memgator " + url + "> memcontent.html"
    os.system(docker_link)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()

    iterate_memgator(args.url)
    #URIM=args.urim
    
    #response = requests.get(URIM)