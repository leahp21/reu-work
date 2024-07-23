import pandas as pd
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.manifold import MDS
from sklearn.feature_extraction.text import TfidfVectorizer
import plotly.express as px

import argparse
import re 
import matplotlib.pyplot as plt
import seaborn as sns


'''
creates term frequency matrix for user hashtags, performs kmeans clustering and MDS, visualizes clusters in plotly
'''
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
    
    # multidimensional scaling to reduce the number of dimensions to 2 (since clustering can only be done on 2 dimensional data)
    mds = MDS(n_components=2)
    new_df_reduced = mds.fit_transform(new_df.drop('Username', axis=1))

    inertias = []

    # elbow method to determine ideal number of clusters
    for i in range(1,len(dictionary)):
        kmeans = KMeans(n_clusters=i)
        kmeans.fit(new_df_reduced)
        inertias.append(kmeans.inertia_)

    plt.plot(range(1,len(dictionary)), inertias, marker='o')
    plt.title('Elbow method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.show()

    # kmeans clustering with n_clusters number determined by elbow method
    kmeans = KMeans(n_clusters=5, random_state=40)
    kmeans.fit(new_df_reduced)
    clusters = kmeans.labels_.astype(str)

    plt.figure(figsize=(10,8))

    df_user_added = pd.DataFrame(new_df_reduced)
    df_user_added['Username'] = new_df['Username']

    print(df_user_added)

    plot = px.scatter(df_user_added, x=0, y=1, color=clusters, hover_name='Username', title="Health Authority and Anti-vax Clustering")

    plt.title("Clustering Users by Hashtags")

    plot.show()

'''
potential groupings of user hashtags. I started this to potentially train a classifier but didn't have enough data. Could be a nice starting point for future
classification of hashtags
'''
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
                 "#citrus", "#capers", "#seafood", "#mushrooms", "#beans", "#nuts", "#wildsalmon", "#keto", "#ketodiet", "#castoroil", "#rice", "#cassava", "#maize", "#noniroot",
                 "#cocoanibs","#cocaonibs", "#wheat", "#eatmoreavocado", "#springwater", "#superherbs", "#cocaopods", "#corn"] 

    disease_hash = ["#aids", "#hpv","#transversemyelitis","#hepatitisb","#multiplesclerosis", "#autism", "#inflammation", "#sids",
                    "#sidsawareness", "#suddendeath","#suddeninfantdeathsyndrome","#cancer", "#diabetes", "#flu",
                    "#infertility", "#breastcancer", "#hypothyroidism", "#dementia", "#headaches", "#depression", "#chronicfatigue", "#seizure",
                    "#decreasedvision", "#bloodpressure", "#autoimmunedisorder", "#hyperthyroidism", "#brainfog", "#hiv", "#defeatmalaria", "#malaria", "#worldaidsday",
                    "#rethinkhiv", "#hivstatus", "#endpolio", "#trypanosomiasis", "#africansleepingsickness", "#infectiousdisease", "#WorldAutismAwarenessDay",
                    "#tb", "#childhoodtb", "#ebola", "#measles", "#diseasedetective", "#breastcancerawareness", "#influenza", "#fasd", "#suicideprevention", "#bcam",
                    "#zika", "#zikavirus", "#virus", "#worldtbday", "#bleedingdisorders", "#autismawareness", "#yellowfever", "#cholera", "#cervicalcancer",
                    "#antimicrobialresistance"]

    health_hash = ["#vitaminc", "#vitamind","#iodine", "#health", "#antibodyenhancement","#vegan", "#vegetarian", "#veganfitness", "#vegetarian", "#plantprotein", "#plantbased",
                   "#centralnervoussystem","#naturalhealth","#brainhealth", "#gut", "#calcium", "#magnesium", "#copper", "#iron", "#zinc", "#protein",
                   "#thyroid", "#kidneys", "#antioxidants","#vitamins","#minerals","#enzymes", "#fiber", "#cholesterol", "#triglycerides", "#healthyfats", 
                   "#relievepain", "#stomach", "#bacteria", "#fungi", "#viruses", "#pathogens", "#illness", "#microbes", "#probiotic", "#anticancer", "#cancerfighter",
                   "#gluten", "#healthy", "#detox", "#holistic", "#chiropractors", "#shoulder", "#injury", "#stemcells", "#bones", "#plant", "#alkaline", "#natural",
                   "#organic", "#diet", "#mri", "#healthylifestyle", "#instahealth", "#gmofree", "#naturalhealing", "#organiclife", "#quitsmoking", "#cancerprevention",
                   "#hearthealth", "#bonehealth", "#healthychoices", "#cancerfighting", "#holistichealing", "#hyperbaricoxygentherapy", "#oxygenflow", 
                   "#tips4health", "#coffeeenema", "#globalhealth", "#menshealthweek", "#MentalHealth", "#NMHW", "#tobaccofree", "#vitals", "#vitalsigns", "#getactive",
                   "#heartage", "#fitness", "#antibiotics", "#stopdrugresistance", "#cervicalhealthmonth", "#humanhealth", "#guthealth", "#stressreduction"]

    covid_hash = ["#coronavirus", "#covid_19", "#covid", "#covidvaccine","#pandemic", "#lockdown", "#twindemic", "#covid", "#covid19", "#wuhan", "#labcreated",
                  "#chinavirus", "#drlimengyan", "#nomasks", "#nomandates", "#coronafalsealarm","#vaxvsunvax","#pland3mic", "#mask", "#contagionmyth", "#maskyourkids",
                  "#noforrealmaskyourkids", "#quarantine", "#inthistogether", "#unprecendentedtimes", "#corona", "#maskmandate", "#ppe", "#covid19sucks", "#kungflu",
                  "#sarscov2", "#flattenthecurb"]
    
    vaccine_hash = ["#vaccine", "#vaccinesafety", "#vaccineinjury", "#vaers", "#hpvvaccine", "#flushot", "#vaccines", "#masteringvaccineinfo",
                    "#vaccinetrials", "#noforcedflushots", "#vaccineeducation", "#vaccineroulette", "#4monthshots","#vaccineriskawareness", "#vaccinesarepoison",
                    "#vaccinefree","#deathaftervaccines","#vaccinations","#noshots","#vaccineskill","#informedconsent", "#learntherisk", "#informedconsent", "#childrenshealthdefense",
                    "#dtap", "#nvic", "#mmr", "#truthaboutvaccines", "#truthaboutcancer", "#thetruthaboutcancer", "#ttac", "#medicalfreedomactivist",
                    "#medicalfreedomofchoice", "#medicalfreedomwarrior", "#medicalfreedom", "#wapf", "#vaccineswork", "#vsd", "#immunizations", "#immunization"]
    
    other_conspiracy = ["#chemtrails", "#chemicalskies", "#geoengineering", "#truther", "#alexjones", "#cloudseeding", "#rockefeller", "#rothschild", "#badscience", "#conspiracy",
                        "#tinfoilhat", "#conspiracytheory", "#conspiracytheorist", "#contagionmyth"]

    pharmaceuticals_hash = ["#bigpharma", "#bigchemical", "#billgates", "#gates","#gatesfoundation",
                            "#pfizer", "#moderna", "#merck", "#gardasil", "#astrazeneca", "#pharma", "#iheartpharma", "#pharma", "#johnsonandjohnson", "#abbvie", "#bayer",
                            "#novartis"]

    gov_hash = ["#anthonyfauci", "#fauci", "#corruption", "#bigbrother", "#censorship", "#censorshipisreal", "#cdc", "#nih", "#fda","#cia", "#surveillance", "#who",
                "#politics", "#tyranny", "#government", "#1984", "#orwell", "#aldoushuxley", "#huxley", "#bravenewworld", "#georgeorwell", "#agenda2030", "#cdcglobal", "#SpotCDC",
                "#cdctips", "#cdcgrandrounds", "#iamcdc", "#gov", "#anarchy", "#nineteeneightyfour", "#rebel", "#rebellion", "#ccp", "#putin", "#capitalism", "#democrats", "#republicans",
                "#republic", "#democracy", "#communism", "#irs", "#feds", "#despot", "#vote", "#voting", "#constitution", "#bureaucrats", "#congress", "#oligarch", "#policestate", "#taxes"]
    

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

'''
determine term frequency for hashtags by counting the number of times a user uses a specific hashtag, divided by the total number of hashtags available for that user
'''
def hash_count_list_function(target_hashtag, dictionary):
    hash_count_list = []

    for key, value_list in dictionary.items():

        hash_count = 0
        
        for hashtag in value_list:

            if hashtag == target_hashtag:
                hash_count += 1

        hash_count = hash_count
        hash_count_list.append(hash_count/len(value_list))

    
    return hash_count_list

'''
make dictionary of hashtags
'''
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

        if len(hashtag_list) != 0:
            hashtag_dictionary[account_name] = hashtag_list
    
    return hashtag_dictionary

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("csv_text_file")
    args = parser.parse_args()

    dictionary = generate_hashtag_dictionary(args.csv_text_file)

    prep_for_clustering(dictionary)
