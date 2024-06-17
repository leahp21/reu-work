import networkx as nx
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math 

def create_graph(hashtag_dict):
    G = nx.Graph()
    color_map = {}
    size_map = {}
    font_map = {}

    for name, hashtag_list in hashtag_dict.items():

        print(name)
        if G.has_node(name) != True:
            G.add_node(name)
            color_map[name] = 'red'
            size_map[name] = 900
            font_map[name] = 12 

        for hashtag in hashtag_list:
            if G.has_node(hashtag):
                G.add_edge(name, hashtag)
            else:
                if (search_for_other_hashtags(hashtag, hashtag_dict) >= 2):
                    G.add_node(hashtag)
                    color_map[hashtag] = 'yellow'
                    size_map[hashtag] = 50
                    font_map[hashtag] = 6
                    G.add_edge(name,hashtag)

    node_colors = [color_map[node] for node in G.nodes]
    node_sizes = [size_map[node] for node in G.nodes]

    pos = nx.spring_layout(G, k=.30)

    plt.figure(3, figsize=(12,12))
    nx.draw(G, with_labels=True, node_color=node_colors, font_size=5, node_size=node_sizes, pos = pos)
    
    plt.show()

def generate_hashtag_dictionary(filename):

    hashtag_dictionary = {}
    csv_list = []

    with open(filename,'r') as csv_files:
        for line in csv_files:
            print(line.split(',')[0])
            csv_list.append(line.split(',')[0])
    

    for csv in csv_list:
        account_name = re.match('^(.+)\.csv$', csv).group(1)

        hashtag_list = []

        df = pd.read_csv('exported_df/anti_vax/'+csv)
        
        for index, row in df.iterrows():
            if pd.notna(row['Hashtags']):
                temp_list = row['Hashtags'].split(',')

                for hash in temp_list:
                    if hash.lower() not in hashtag_list:
                        hashtag_list.append(hash.lower())
        
        hashtag_dictionary[account_name] = hashtag_list
    
    return hashtag_dictionary

def search_for_other_hashtags(hashtag, dictionary):
    hashtag_count = 0

    for key, value in dictionary.items():

        for each in value:
            if each == hashtag:
                hashtag_count += 1
    
    return hashtag_count

if __name__ == "__main__":
    # get csv names, s

    filename="csv_list.txt"
    dict = generate_hashtag_dictionary(filename)
    create_graph(dict)