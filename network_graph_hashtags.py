import networkx as nx
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math 
import argparse
import sys

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

        for hashtag in hashtag_list[0]:
            if G.has_node(hashtag):
                G.add_edge(name, hashtag)
                size_map[hashtag] += 50
            else:
                if (search_for_other_hashtags(hashtag, name, hashtag_dict) == True):
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
        account_name = re.search('([^\/]+)\.csv$', csv).group(1)
        affiliation = re.search('[^\/]+\/([^\/]+)\/[^\/]+',csv).group(1)

        hashtag_list = []

        df = pd.read_csv(csv)
        df = df.drop_duplicates(subset=['Follower_count', 'Comment_count', 'Like_count','Hashtags', 'Hashtag_count', 'Mentions', 'Mention_count'], keep='first')
        df = df.dropna(thresh=2)
        
        for index, row in df.iterrows():
            if pd.notna(row['Hashtags']):
                temp_list = row['Hashtags'].split(',')

                for hash in temp_list:
                    if hash not in hashtag_list:
                        hashtag_list.append(hash.lower())
        
        hashtag_dictionary[account_name] = [hashtag_list, affiliation]
    
    return hashtag_dictionary

def search_for_other_hashtags(hashtag, person_name, dictionary):
    hashtag_count = False

    # for each hashtag, check if the hashtag is in another's value

    for name in dictionary.keys():
        if person_name != name:
            if hashtag in dictionary[name]:
                return True
    
    return hashtag_count

def co_occur_graph(hashtag_dict):
    one_group = []
    list_of_keys = list(hashtag_dict.keys())
    one_group.append(list_of_keys[0])

    other_group = []
    
    for key,value in hashtag_dict.items():
        if value[1] == hashtag_dict[one_group[0]][1]:
            print("yay")
            one_group.append(key)
        else:
            other_group.append(key)

    G = nx.Graph()
    color_map = {}
    size_map = {}
    font_map = {}

    for name in hashtag_dict.keys():

        if G.has_node(name) != True:
            G.add_node(name)
            color_map[name] = 'red'
            size_map[name] = 900
            font_map[name] = 12 

    for name in one_group:

        for hashtag in hashtag_dict[name][0]:
        
            for other_name in other_group:

                if hashtag in hashtag_dict[other_name][0]:
                    if G.has_node(hashtag):
                        G.add_edge(other_name, hashtag)
                        G.add_edge(name, hashtag)
                        size_map[hashtag] += 50
                    else:
                        G.add_node(hashtag)
                        color_map[hashtag] = 'yellow'
                        size_map[hashtag] = 50
                        font_map[hashtag] = 6
                        G.add_edge(name,hashtag)
                        G.add_edge(other_name,hashtag)

    node_colors = [color_map[node] for node in G.nodes]
    node_sizes = [size_map[node] for node in G.nodes]

    pos = nx.spring_layout(G, k=.30)

    plt.figure(3, figsize=(12,12))
    nx.draw(G, with_labels=True, node_color=node_colors, font_size=5, node_size=node_sizes, pos = pos)

    plt.show()



if __name__ == "__main__":
    # get csv names, s
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", action="store_true")
    parser.add_argument("csv_files")
    args = parser.parse_args()

    filename=args.csv_files
    print(args)
   
    dict = generate_hashtag_dictionary(filename)

    if(sys.argv == 1):
        create_graph(dict)
    else:
        co_occur_graph(dict)