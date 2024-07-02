import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import argparse
import re 
import matplotlib.pyplot as plt

def map_non_numeric(dictionary):

    new_df = pd.DataFrame()

    '''

    food_hash = ["#seeds", "#food","#gmos","#avocado", "#kale", "#soup", "#soyfoods","#salad", "#wholefoods", "#superfood", "#superfoodsalad",
                 "#walnuts", "#beets", "#cucumber", "#asparagus", "#redpepper", "#apple", "#artichoke", "#spinach", "#realoliveoil", "#vinegarette",
                 "#lunchtime", "#highfructosecornsyrup", "#dressings","#pea", "#nutrition", "#greentea", "#matcha", "#fermentedveggies", "#fermentedfoods",
                 "#sauerkraut", "#coffee","#matchagreentea", "#avocados","#hassavocado","#healthysnack", "#healthyfood", "#almonds", "#cacao",
                 "#bonebroth", "#coconutoil", "#trailmix", "#driedcoconut", "#driedcranberries", "#pistachio", "#cashews", "#pumpkinseeds", "#mullberry", 
                 "#gojiberries", "#goldenraisins", "#greenjuice", "#vegetablejuice", "#carrots", "#cabbage", "#onions",
                 "#brusselssprouts", "#leeks"]

    disease_hash = ["#aids", "#hpv","#transversemyelitis","#hepatitisb","#multiplesclerosis", "#autism", "#inflammation", "#sids",
                    "#sidsawareness", "#suddendeath","#suddeninfantdeathsyndrome","#cancer", "#diabetes", "#flu",
                    "#infertility", "#breastcancer", "#hypothyroidism", "#dementia"]

    health_hash = ["#vitaminc", "#vitamind","#iodine", "#health", "#antibodyenhancement","#vegan", "#veganfitness", "#vegetarian", "#plantprotein", "#plantbased",
                   "#centralnervoussystem","#naturalhealth","#brainhealth", "#gut", "#calcium", "#magnesium", "#copper", "#iron", "#zinc", "#protein",
                   "#thyroid", "#kidneys", "#antioxidants","#vitamins","#minerals","#enzymes", "#fiber", "#cholesterol", "#triglycerides", "#healthyfats", 
                   "#relievepain", "#stomach", "#bacteria", "#fungi", "#viruses", "#pathogens", "#illness", "#microbes", "#probiotic", "#anticancer", "#cancerfighter"]

    covid_hash = ["#coronavirus", "#covid_19", "#covid", "#covidvaccine","#pandemic", "#lockdown", "#twindemic", "#covid", "#covid19", "#wuhan", "#labcreated",
                  "#chinavirus", "#drlimengyan", "#nomasks", "#nomandates", "#coronafalsealarm","#vaxvsunvax","#pland3mic"]
    
    vaccine_hash = ["#vaccine", "#vaccinesafety", "#vaccineinjury", "#vaers", "#hpvvaccine", "#flushot", "#vaccines", "#masteringvaccineinfo",
                    "#vaccinetrials", "#noforcedflushots", "#vaccineeducation", "#vaccineroulette", "#4monthshots","#vaccineriskawareness", "#vaccinesarepoison",
                    "#vaccinefree","#deathaftervaccines","#vaccinations","#noshots","#vaccineskill","#informedconsent", "#learntherisk"]

    pharmaceuticals_hash = ["#bigpharma", "#bigchemical", "#billgates", "#gates","#gatesfoundation", "#informedconsent",
                            "#pfizer", "#moderna", "#merck", "#gardasil", "#astrazeneca", "#pharma"]

    gov_hash = ["#anthonyfauci", "#fauci", "#corruption", "#bigbrother", "#censorship", "#censorshipisreal", "#cdc", "#nih", "#fda","#cia", "#surveillance", "#who"]

    ''' 

    for key, value_list in dictionary.items():

        for value in value_list:
            new_df = new_df.append({"Username": key, "Hashtag": value}, ignore_index=True)

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 2)
    pd.set_option('display.width', 150)

    print(new_df)


    ''' machine learning stuff '''
    X = new_df
    y = new_df['Username']

    le = LabelEncoder()

    cols = X.columns

    X['Username'] = le.fit_transform(X['Username'])
    X['Hashtag'] = le.fit_transform(X['Hashtag'])

    ms = MinMaxScaler()

    X = ms.fit_transform(X)

    X = pd.DataFrame(X, columns=[cols])

    print(X, y)


# Convert the scaled features back to a DataFrame


    cs = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
        kmeans.fit(X)
        cs.append(kmeans.inertia_)

    
    plt.plot(range(1, 11), cs)
    plt.title('The Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('CS')
    plt.show()

    

    kmeans = KMeans(n_clusters=3,random_state=0)
    kmeans.fit(X)

    plt.scatter(X[X.columns[1]], X[X.columns[0]], c=kmeans.labels_)
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

        hashtag_list = []

        df = pd.read_csv(csv)
        
        for index, row in df.iterrows():
            if pd.notna(row['Hashtags']):
                temp_list = row['Hashtags'].split(',')

                for hash in temp_list:
                    if hash.lower() not in hashtag_list:
                        hashtag_list.append(hash.lower())
        
        hashtag_dictionary[account_name] = hashtag_list
    
    return hashtag_dictionary

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("csv_text_file")
    args = parser.parse_args()

    dictionary = generate_hashtag_dictionary(args.csv_text_file)

    map_non_numeric(dictionary)
