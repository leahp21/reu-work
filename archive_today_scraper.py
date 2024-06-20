import requests
from bs4 import BeautifulSoup
import json
import re
import argparse
import sys

'''
initially tried this link: https://archive.ph/A4ya8
'''

'''
gets the user's bio using bs4
'''
def get_bio(soup, profile_dict):
    possible_bio_list = soup.find('section').find('section').find_all('div')
    bio = "no bio"

    # gets bio for users. depends on if they have their name and Public figure status set
    if (possible_bio_list[-2].get_text() == ""):
        if possible_bio_list[-1].find_all('span') != None:
            bio = possible_bio_list[-1].find_all('span')[-1].get_text()
    else:
        if (len(possible_bio_list) >= 2):
            if len(possible_bio_list[-2].find_all('span')) != 0:
                bio = possible_bio_list[-2].find_all('span')[-1].get_text()
    
    profile_dict['bio'] = bio

    return profile_dict

'''
gets the user's username
'''
def get_username(soup, profile_dict):

    username = soup.find('section')

    # if username is empty (as in the html page is empty) exit the program
    if (username == None):
        sys.exit()

    if username.find('h2') == None:
        profile_dict['username'] = username.find('h1').get_text()
    else:
        profile_dict["username"] = username.find('h2').get_text()

    return profile_dict

'''
    gets the follower count 
'''
def get_followers(soup, profile_dict):
    follower_count = None

    possible_follower_count = soup.find('section').find('ul').find_all('a')
    
    # gets the followers for users 2022 and back
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

'''
gets the post count of the user
'''
def get_post_count(soup, profile_dict):
    post_count = soup.find('section').find('li').get_text()
    profile_dict['post_count'] = post_count

    return profile_dict

'''
gets post content (alt-text and media type)
'''
def get_post_content(soup, profile_dict):

    post_dictionary = {}
    post_count = 1

    insta_body = soup.find('article').find_all('div')

    # for all possible posts, find the post link, image alt-text and media type of post 
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

'''
get the year of the memento (is important for cases)
'''
def get_memento_date(soup, user_profile_dict):
    archive_date_str = soup.find('span').get_text()
    date = re.search('archived\s([^>]+)',archive_date_str).group(1)
    split_date = date.split(" ")
    memento_year = split_date[2]

    user_profile_dict['date'] = memento_year

    return user_profile_dict

'''
converts dictionary of account details to json file and std.out
'''
def write_dict_to_json(dictionary):
    filename = dictionary["username"] + '.json'
    json_out = open(filename, 'w')
    json_out.write(json.dumps(dictionary, indent=4))
    json_out.close()

    sys.stdout.write(json.dumps(dictionary, indent=4))

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

    user_profile_dict = {}

    user_profile_dict = get_memento_date(soup, user_profile_dict)

    user_profile_dict = get_username(soup,user_profile_dict)
    user_profile_dict = get_followers(soup, user_profile_dict)
    user_profile_dict = get_post_count(soup, user_profile_dict)

    user_profile_dict = get_bio(soup, user_profile_dict)
    user_profile_dict = get_post_content(soup, user_profile_dict)
    write_dict_to_json(user_profile_dict)

    