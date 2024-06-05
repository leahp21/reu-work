import requests
from bs4 import BeautifulSoup
import json
import re
import argparse
import sys


def get_bio(soup):
    possible_list = soup.find_all('span')
    i = 0

    # need to check for dates

    if possible_list[1].get_text() == "no other snapshots from this url":
        bio = possible_list[8].get_text()
    elif possible_list[7].get_text() == ".":
        bio = possible_list[12].get_text()
    else:
        bio = possible_list[7].get_text()

    for each in possible_list:
        i += 1

    print(bio)

def get_post_content(soup):
    post_dictionary = {}
    post_count = 1

    insta_body = soup.find('article').find_all('div')

    for post in insta_body:
        dict_key_name = "postNum" + str(post_count)

        post_content = post.find('a')
        
        if(post_content) != None:
            post_link = post_content.get('href')
            
            img_text = post_content.find('img').get('alt')
            if (post_content.find('span') != None):
                post_type = post_content.find('span').get('aria-label')
            if post_type == None:
                post_type = 'Photo'

            post_dictionary[dict_key_name] = []

            post_dictionary[dict_key_name].append(post_link)
            post_dictionary[dict_key_name].append(img_text)
            post_dictionary[dict_key_name].append(post_type)

            post_count += 1
        
    return post_dictionary
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--urim", type=str)
    args=parser.parse_args()
    URIM=args.urim
    
    response = requests.get(URIM)
    html = response.text
    soup = BeautifulSoup(html, "lxml")

    get_bio(soup)
    print(get_post_content(soup))

    html_out = open("hashtag.html", "w")
    html_out.write(str(soup.prettify()))
    html_out.close()
