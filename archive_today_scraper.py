import requests
from bs4 import BeautifulSoup
import json
import re
import argparse
import sys

'''
initially tried this link: https://archive.ph/A4ya8
'''

def get_bio(soup, profile_dict, mem_date):
    possible_bio_list = soup.find('section').find('section').find_all('div')
    bio = "no bio"

    for div_tag in possible_bio_list:
        if (div_tag.find('h1') != None):
            if div_tag.find('span') != None:
                bio = div_tag.find('span').get_text()

    if mem_date >= 2021:
        bio = possible_bio_list[-3].get_text()
    # need to check for dates

    '''
    if possible_list[1].get_text() == "no other snapshots from this url":
        bio = possible_list[8].get_text()
    elif possible_list[7].get_text() == ".":
        bio = possible_list[12].get_text()
    else:
        bio = possible_list[7].get_text()
    '''

    profile_dict['bio'] = bio

    return profile_dict

def get_username(soup, profile_dict):
    username = soup.find('section').find('h2').get_text()
    profile_dict["username"] = username

    return profile_dict
    
def get_followers(soup, profile_dict):
    follower_count = None

    possible_follower_count = soup.find('section').find('ul').find_all('a')
    
    for text in possible_follower_count:
        maybe_match = text.get_text()
        if "followers" in maybe_match:
            follower_count = maybe_match

    #2023 forward

    if follower_count == None:
        possible_follower_count = soup.find('section').find('section').find('ul').find_all('li')
        follower_count = possible_follower_count[1].get_text()

    profile_dict['follower_count'] = follower_count

    return profile_dict

def get_post_count(soup, profile_dict):
    post_count = soup.find('section').find('li').get_text()
    profile_dict['post_count'] = post_count

    return profile_dict

def get_post_content(soup, profile_dict):

    post_dictionary = {}
    post_count = 1

    insta_body = soup.find('article').find_all('div')

    for post in insta_body:

        post_content = post.find('a')

        if(post_content) != None and post.find('div').find('a') == None:
            dict_key_name = "postNum" + str(post_count)

            post_link = post_content.get('href')

            img_text = post_content.find('img').get('alt')

            if post_content.find('span') != None:
                post_type = post_content.find('span').get('aria-label')
            elif (post_content.find('svg') != None):
                post_type = post_content.find('svg').get('aria-label')
            else:
                post_type = 'Photo'

            post_dictionary[dict_key_name] = {}

            post_dictionary[dict_key_name].update({"post-link": post_link})
            post_dictionary[dict_key_name].update({"image-text": img_text})
            post_dictionary[dict_key_name].update({"post-type": post_type})

            post_count += 1

    profile_dict["Posts"] = post_dictionary
        
    return profile_dict



def get_memento_date(soup):
    archive_date_str = soup.find('span').get_text()
    date = re.search('archived\s([^>]+)',archive_date_str).group(1)
    split_date = date.split(" ")
    memento_year = int(split_date[2])
    return memento_year

def write_dict_to_json(dictionary):
    filename = dictionary["username"] + '.json'
    json_out = open(filename, 'w')
    json_out.write(json.dumps(dictionary, indent=4))
    json_out.close()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--urim", type=str)
    args=parser.parse_args()
    URIM=args.urim
    
    response = requests.get(URIM)
    html = response.text
    soup = BeautifulSoup(html, "lxml")

    html_out = open("hashtag.html", "w")
    html_out.write(str(soup.prettify()))
    html_out.close()

    archive_date = get_memento_date(soup)

    user_profile_dict = {}

    user_profile_dict = get_username(soup,user_profile_dict)
    user_profile_dict = get_followers(soup, user_profile_dict)
    user_profile_dict = get_post_count(soup, user_profile_dict)

    user_profile_dict = get_bio(soup, user_profile_dict,archive_date)
    user_profile_dict = get_post_content(soup, user_profile_dict)
    write_dict_to_json(user_profile_dict)

    