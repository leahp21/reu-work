***2024 ODU Disinformation Detection and Analytics REU***

Here are some cool files for you to check out!

- archive_today_scraper.py
- process_memento.py
- network_graph_mentions.py
- network_graph_hashtags.py

**Archive_today_scraper**

This script scrapes page content of a Instagram memento from archive.today/archive.ph/archive.is/archive.md as long as the memento is
from 2019-2023. The output is a JSON file which contains the username, bio, post type, and some post content (depending on the media type of the post).
The json file is named after the user whose profile is being scraped. Some examples of the output are in the archive_today_scraper_outputs folder.

Example usage:

```
python3 archive_today_scraper.py --urim https://archive.ph/ze2v6
```
```
python3 archive_today_scraper.py --urim [archive_today_memento_urim]
```

**Process_memento**

This script finds all of the available mementos for a given URI-R (using memgator), scrapes the mementos, then extracts the hashtags, account mentions, 
like count, and follower count. Those details and the memento-datetimes are stored in a Pandas dataframe. The dataframe is exported to a CSV file and the 
CSV file is named after the Instagram user whose profile is being examined. Some examples of the output are in the exported_df folder. 

Example usage:

```
python3 process_memento.py www.instagram.com/robertfkennedyjr/
```
```
python3 process_memento.py [instagram_uri-r]
```
