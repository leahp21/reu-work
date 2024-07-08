import pandas as pd
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from scipy.cluster.hierarchy import dendrogram, linkage
import argparse
import re 
import matplotlib.pyplot as plt
import seaborn as sns

def prep_for_clustering(dictionary):

    new_df = pd.DataFrame()

    new_dict = {'Username': dictionary.keys()}

    new_df = pd.DataFrame.from_dict(new_dict)


    for key, value_list in dictionary.items():

        for value in value_list:
            if value not in new_df.columns:
                new_df[value] = hash_count_list_function(value, dictionary)


    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 150)

    print(new_df)

    '''
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(new_df.drop('Username', axis=1))
    clusters = kmeans.labels_
    '''

    Z = linkage(new_df.drop('Username', axis=1), method='ward')
    new_df.set_index('Username', inplace=True)

    plt.figure(figsize=(10, 8))
    dendrogram(Z, labels=new_df.index, leaf_rotation=90)
    plt.title('Dendrogram')
    plt.xlabel('Words')
    plt.ylabel('Distance')
    plt.show()

# Convert the scaled features back to a DataFrame

def classify_hashtags(dictionary):

    new_df = pd.DataFrame()

    food_hash = ["#seeds", "#food","#gmos","#avocado", "#kale", "#soup", "#soyfoods","#salad", "#wholefoods", "#superfood", "#superfoodsalad",
                 "#walnuts", "#beets", "#cucumber", "#asparagus", "#redpepper", "#apple", "#artichoke", "#spinach", "#realoliveoil", "#vinegarette",
                 "#lunchtime", "#highfructosecornsyrup", "#dressings","#pea", "#nutrition", "#greentea", "#matcha", "#fermentedveggies", "#fermentedfoods",
                 "#sauerkraut", "#coffee","#matchagreentea", "#avocados","#hassavocado","#healthysnack", "#healthyfood", "#almonds", "#cacao",
                 "#bonebroth", "#coconutoil", "#trailmix", "#driedcoconut", "#driedcranberries", "#pistachio", "#cashews", "#pumpkinseeds", "#mullberry", 
                 "#gojiberries", "#goldenraisins", "#greenjuice", "#vegetablejuice", "#carrots", "#cabbage", "#onions",
                 "#brusselssprouts", "#leeks", "#smoothie", "#raw", "#blueberries","#bananas", "#banana", "#juice", "#chocolate", "#fruit", "#coconut",
                 "#mint", "#pie", "#wine", "#strawberries", "#sweetpotato", "#turmeric", "#curcumin", "#goldenmilk", "#gmo", "#pudding",
                 "#carrot", "#dessert", "#veggies", "#honey", "#veggie", "#rawfood", "#lemon", "#falafel", "#garlic", "#cumin", "#salt", "#sesameseeds", "#soy", "#nogmo",
                 "#sugar", "#watermelon", "#celery", "#broccoli", "#cantaloupe", "#radish", "#tomato", "#hymalayansalt", "#blackcuminseed", "#maca",
                 "#citrus", "#capers", "#seafood", "#mushrooms", "#beans", "#nuts", "#wildsalmon", "#keto", "#ketodiet", "#castoroil", "#rice", "#cassava", "#maize"] 

    disease_hash = ["#aids", "#hpv","#transversemyelitis","#hepatitisb","#multiplesclerosis", "#autism", "#inflammation", "#sids",
                    "#sidsawareness", "#suddendeath","#suddeninfantdeathsyndrome","#cancer", "#diabetes", "#flu",
                    "#infertility", "#breastcancer", "#hypothyroidism", "#dementia", "#headaches", "#depression", "#chronicfatigue", "#seizure",
                    "#decreasedvision", "#bloodpressure", "#autoimmunedisorder", "#hyperthyroidism", "#brainfog", "#hiv", "#defeatmalaria", "#malaria", "#worldaidsday",
                    "#rethinkhiv", "#hivstatus", "#endpolio", "#trypanosomiasis", "#africansleepingsickness", "#infectiousdisease"]

    health_hash = ["#vitaminc", "#vitamind","#iodine", "#health", "#antibodyenhancement","#vegan", "#vegetarian", "#veganfitness", "#vegetarian", "#plantprotein", "#plantbased",
                   "#centralnervoussystem","#naturalhealth","#brainhealth", "#gut", "#calcium", "#magnesium", "#copper", "#iron", "#zinc", "#protein",
                   "#thyroid", "#kidneys", "#antioxidants","#vitamins","#minerals","#enzymes", "#fiber", "#cholesterol", "#triglycerides", "#healthyfats", 
                   "#relievepain", "#stomach", "#bacteria", "#fungi", "#viruses", "#pathogens", "#illness", "#microbes", "#probiotic", "#anticancer", "#cancerfighter",
                   "#gluten", "#healthy", "#detox", "#holistic", "#chiropractors", "#shoulder", "#injury", "#stemcells", "#bones", "#plant", "#alkaline", "#natural",
                   "#organic", "#diet", "#mri", "#healthylifestyle", "#instahealth", "#gmofree", "#naturalhealing", "#organiclife", "#quitsmoking", "#cancerprevention",
                   "#hearthealth", "#bonehealth", "#healthychoices", "#cancerfighting", "#holistichealing", "#hyperbaricoxygentherapy", "#oxygenflow", 
                   "#tips4health", "#coffeeenema", "#globalhealth"]

    covid_hash = ["#coronavirus", "#covid_19", "#covid", "#covidvaccine","#pandemic", "#lockdown", "#twindemic", "#covid", "#covid19", "#wuhan", "#labcreated",
                  "#chinavirus", "#drlimengyan", "#nomasks", "#nomandates", "#coronafalsealarm","#vaxvsunvax","#pland3mic", "#mask", "#contagionmyth", "#maskyourkids",
                  "#noforrealmaskyourkids", ]
    
    vaccine_hash = ["#vaccine", "#vaccinesafety", "#vaccineinjury", "#vaers", "#hpvvaccine", "#flushot", "#vaccines", "#masteringvaccineinfo",
                    "#vaccinetrials", "#noforcedflushots", "#vaccineeducation", "#vaccineroulette", "#4monthshots","#vaccineriskawareness", "#vaccinesarepoison",
                    "#vaccinefree","#deathaftervaccines","#vaccinations","#noshots","#vaccineskill","#informedconsent", "#learntherisk", "#informedconsent", "#childrenshealthdefense",
                    "#dtap", "#nvic", "#mmr", "#truthaboutvaccines", "#truthaboutcancer", "#thetruthaboutcancer", "#ttac", "#medicalfreedomactivist",
                    "#medicalfreedomofchoice", "#medicalfreedomwarrior", "#medicalfreedom", "#wapf", "#vaccineswork"]
    
    other_conspiracy = ["#chemtrails", "#geoengineering", "#truther", "#alexjones", "#cloudseeding", "#rockefeller", "#rothschild", "#badscience"]

    pharmaceuticals_hash = ["#bigpharma", "#bigchemical", "#billgates", "#gates","#gatesfoundation",
                            "#pfizer", "#moderna", "#merck", "#gardasil", "#astrazeneca", "#pharma", "#iheartpharma"]

    gov_hash = ["#anthonyfauci", "#fauci", "#corruption", "#bigbrother", "#censorship", "#censorshipisreal", "#cdc", "#nih", "#fda","#cia", "#surveillance", "#who",
                "#politics", "#tyranny", "#government", "#1984", "#orwell", "#aldoushuxley", "#huxley", "#bravenewworld", "#georgeorwell", "#agenda2030", ]
    

    for key, value_list in dictionary.items():

        vaccine_count = 0
        gov_count = 0
        pharma_count = 0
        covid_count = 0
        health_count = 0
        disease_count = 0
        food_count = 0
        other_conspiracy_count = 0
        extra_count = 0

        for value in value_list:
            if value in food_hash:
                food_count += 1
            elif value in vaccine_hash:
                vaccine_count += 1
            elif value in gov_hash:
                gov_count += 1
            elif value in pharmaceuticals_hash:
                pharma_count += 1
            elif value in covid_hash:
                covid_count += 1
            elif value in health_hash:
                health_count += 1
            elif value in disease_hash:
                disease_count += 1
            elif value in other_conspiracy:
                other_conspiracy_count += 1
            else:
                extra_count += 1
        
        total = vaccine_count + gov_count + pharma_count + covid_count +health_count + disease_count + food_count + other_conspiracy_count + extra_count

        new_df = new_df.append({'Username': key, 'Vaccine Count': vaccine_count, 'Pharmaceutical Count': pharma_count, 'COVID Count': covid_count, 'Health Count': health_count, 'Health Condition Count': disease_count,
                       'Food Count': food_count, 'Conspiracy Count': other_conspiracy_count, 'Extraneous Count': extra_count, 'Total Count':total}, ignore_index=True)
        
        new_df.set_index('Username')
        
    print (new_df)


def hash_count_list_function(target_hashtag, dictionary):
    hash_count_list = []

    for key, value_list in dictionary.items():
        hash_count = 0

        for hash in value_list:
            if hash == target_hashtag:
                hash_count += 1
        
        hash_count_list.append(hash_count)
    
    return hash_count_list


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
        df.drop_duplicates
        
        for index, row in df.iterrows():
            if pd.notna(row['Hashtags']):
                temp_list = row['Hashtags'].split(',')

                for hash in temp_list:
                    hashtag_list.append(hash.lower())
        
        hashtag_dictionary[account_name] = hashtag_list
    
    return hashtag_dictionary

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("csv_text_file")
    args = parser.parse_args()

    dictionary = generate_hashtag_dictionary(args.csv_text_file)

    prep_for_clustering(dictionary)
    # classify_hashtags(dictionary)
