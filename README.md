***2024 ODU Disinformation Detection and Analytics REU***

Here are some cool files for you to check out!

- archive_today_scraper.py
- process_memento.py
- network_graph_mentions.py
- network_graph_hashtags.py
- cluster_hashtags.py

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

In order for this program to run, you need to download Memgator, which can be downloaded here: https://github.com/oduwsdl/MemGator. This script finds all of the available mementos for a given URI-R (using memgator), scrapes the mementos, then extracts the hashtags, account mentions, 
like count, and follower count. Those details and the memento-datetimes are stored in a Pandas dataframe. The dataframe is exported to a CSV file and the 
CSV file is named after the Instagram user whose profile is being examined. Some examples of the output are in the exported_df folder. 

Example usage:

```
python3 process_memento.py www.instagram.com/robertfkennedyjr/
```
```
python3 process_memento.py [instagram_uri-r]
```

**Cluster_hashtags**

This script takes a text file of user CSV's and creates a term frequency matrix for the hashtags that a user uses. Multidimensional scaling reduces the number of dimensions from the number of
user hashtags to 2, and KMeans clustering is performed based on the hashtags. Plotly generates an interactive scatterplot that contains clusters of the users and their names. An example of
the output is health_and_anti_clustering.png, which is located in graph_and_charts. 

Example usage:

```
python3 cluster_hashtags.py health_and_anti.txt
```

```
python3 cluster_hashtags.py [list_of_csvs]
```

**Mention and Hashtag network graphs**

The Mention and Hashtag network graphs are in two separate scripts: network_graphs_mentions.py and network_graphs_hashtags.py. Both scripts require a text file of CSV's. The scripts create social
networks by connecting users by the hashtags and mentions that they have in common. The hashtag node size is adjusted based on frequency. An example of the hashtag graph is the output is health_and_anti_total_graph.png, which is located in graph_and_charts. 