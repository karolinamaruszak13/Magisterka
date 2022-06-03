import matplotlib.pyplot as plt
import pandas as pd
from common import getDbCursor, vaccines_dict, getCountryNames

myCursor = getDbCursor()
country_names = getCountryNames()
def getCount(vaccine_name):
    myCursor.execute(f"select p.country_code, count(*) FROM tweets t \
    left join places p \
    on p.id = t.place_id \
    WHERE  t.place_id is not NULL and \
    lower(tweet_text) like '%{vaccine_name}%'\
    group by p.country_code \
    order by 2 desc")
    print('Fetching', vaccines_dict[vaccine_name]['display_name'])
    touple_list = myCursor.fetchall()
    data = list(zip(*touple_list))
    return data

def getAllCounts(vaccines_names):
    counts = {}
    for vaccine_name in vaccines_names:
        counts[vaccine_name] = getCount(vaccine_name)
    return counts

def plot_vaccine_pre_country(vaccine_name, data, max_countries):
    x_labels = [country_names[code] for code in data[0][:max_countries]]
    rects = plt.bar(x_labels, data[1][:max_countries], color=vaccines_dict[vaccine_name]['color'])
    plt.bar_label(rects)
    plt.xticks(rotation=90)
    display_name = vaccines_dict[vaccine_name]['display_name']    
    plt.xlabel('Nazwa kraju')
    plt.ylabel('Liczba tweetów')
    plt.title(f"Popularność tweetów dotyczących {display_name} w danym kraju")
    plt.tight_layout()
    plt.savefig(f'charts/{display_name}_popularity_by_country.png')
    plt.close()

def plot_all_vaccines_per_country(vaccine_counts_per_country, max_countries):
    for vaccine_name, data in vaccine_counts_per_country.items():
        plot_vaccine_pre_country(vaccine_name, data, max_countries)

counts = getAllCounts(vaccines_dict.keys())
plot_all_vaccines_per_country(counts, 20)