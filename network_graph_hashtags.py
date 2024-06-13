import networkx as nx
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_graph(hashtag_dict):
    G = nx.Graph()

    for name, hashtag_list in hashtag_dict.items():
        print(name)
        if G.has_node(name) != True:
            G.add_node(name, node_color='red', node_size=3000)

        for hashtag in hashtag_list:
            if G.has_node(hashtag):
                G.add_edge(name, hashtag)
            else:
                G.add_node(hashtag, node_color='blue', node_size=1500)
                G.add_edge(name,hashtag)
    
    nx.draw(G, with_labels=True, font_size=7)
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

if __name__ == "__main__":
    # get csv names, s

    filename="csv_list.txt"
    dict = generate_hashtag_dictionary(filename)
    create_graph(dict)