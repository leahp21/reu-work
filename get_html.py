import requests
from bs4 import BeautifulSoup
import argparse
import re
import sys

def archive_today_or_wb(url, web_text):
    username = ""
    return_file = ""

    if ("archive.ph" in url):
        pattern = re.compile('username*\=([A-Za-z0-9._]+)')
        username = pattern.match(web_text.get_text())
        print(web_text.get_text())
        return_file = str(username) + "_archiveToday.html"

    return return_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--urim", type=str)
    args=parser.parse_args()
    URIM=args.urim
    
    response = requests.get(URIM)
    html = response.text
    soup = BeautifulSoup(html, "lxml")

    out_file = archive_today_or_wb(URIM, soup)

    html_out = open(out_file, "w")
    html_out.write(str(soup))
    html_out.close()
