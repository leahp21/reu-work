import networkx as nx
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math 
import argparse
import sys
import seaborn as sns

def create_graph(hashtag_dict):
    G = nx.Graph()
    color_map = {}
    size_map = {}
    font_map = {}

    plt.figure(figsize=(8, 6))

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

    # go through all of the nodes, if node is a hashtag node, 

    H = nx.MultiGraph()

    for name, hashtag in hashtag_dict.items():
        H.add_node(name)

    for node in G.nodes:
        if '#' in node:
            neighbors = list(G.neighbors(node))
            for i in range(len(neighbors)):
                for j in range(i+1, len(neighbors)):
                    H.add_edge(neighbors[i], neighbors[j])

    node_mapping = {node: idx for idx, node in enumerate(H.nodes())}

    n = len(H.nodes)
    adj_matrix = np.zeros((n, n))

    for u, v in H.edges():
        adj_matrix[node_mapping[u], node_mapping[v]] += 1
        adj_matrix[node_mapping[v], node_mapping[u]] += 1 

    pd.set_option("display.precision", 0) 

    node_labels = [node for node in H.nodes()]

    ax = sns.heatmap(adj_matrix, annot=True, cmap='coolwarm', center=5, xticklabels=node_labels, yticklabels=node_labels, fmt='g')

    ax.set_xticklabels(node_labels, rotation=45, ha='right')

    plt.title("Connecting Instagram Accounts through Co-occuring Hashtag Frequency")
    plt.tight_layout()
    
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
            if hashtag in dictionary[name][0]:
                return True
    
    return hashtag_count

def co_occur_graph(hashtag_dict):
    one_group = []
    list_of_keys = list(hashtag_dict.keys())
    one_group.append(list_of_keys[0])

    other_group = []
    
    for key,value in hashtag_dict.items():
        if value[1] == hashtag_dict[one_group[0]][1]:
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
    
    H = nx.MultiGraph()

    for name, hashtag in hashtag_dict.items():
        H.add_node(name)

    for node in G.nodes:
        if '#' in node:
            neighbors = list(G.neighbors(node))
            for i in range(len(neighbors)):
                for j in range(i+1, len(neighbors)):
                    H.add_edge(neighbors[i], neighbors[j])

    node_mapping = {node: idx for idx, node in enumerate(H.nodes())}

    n = len(H.nodes)
    adj_matrix = np.zeros((n, n))

    for u, v in H.edges():
        adj_matrix[node_mapping[u], node_mapping[v]] += 1
        adj_matrix[node_mapping[v], node_mapping[u]] += 1 

    pd.set_option("display.precision", 0) 

    #adj_matrix = nx.adjacency_matrix(H).todense()

    node_labels = [node for node in H.nodes()]

    ax = sns.heatmap(adj_matrix, annot=True, cmap='coolwarm', center=5, xticklabels=node_labels, yticklabels=node_labels, fmt='g')

    ax.set_xticklabels(node_labels, rotation=45, ha='right')

    plt.title("Connecting Instagram Accounts through Co-occuring Hashtag Frequency")
    plt.tight_layout()
    
    plt.show()



if __name__ == "__main__":
    # get csv names, s
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", action="store_true")
    parser.add_argument("csv_files")
    args = parser.parse_args()

    filename=args.csv_files
   
    dict = generate_hashtag_dictionary(filename)

    if args.c == False:
        create_graph(dict)
    else:
        print('yay')
        co_occur_graph(dict)
