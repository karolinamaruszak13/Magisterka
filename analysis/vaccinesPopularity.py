import matplotlib.pyplot as plt
from common import getDbCursor, vaccines_dict

myCursor = getDbCursor()

def getCount(vaccine_name):
    myCursor.execute(f"select count(*) from tweets where lower(tweet_text) like '%{vaccine_name}%'")
    print('Fetching', vaccines_dict[vaccine_name]['display_name'])
    return myCursor.fetchone()[0]

def getAllCounts(vaccines_names):
    counts = []
    for vaccine_name in vaccines_names:
        counts.append(getCount(vaccine_name))
    return counts


vaccines_count = getAllCounts(vaccines_dict.keys())
print(vaccines_count)
vaccines_names = list(map(lambda x: x['display_name'], vaccines_dict.values()))
vaccines_colors = list(map(lambda x: x['color'], vaccines_dict.values()))
plt.figure(figsize=(15,10))
rects = plt.bar(vaccines_names, vaccines_count, width=0.6, color=vaccines_colors)
plt.bar_label(rects, fontsize='xx-large')
plt.ylabel('Liczba tweetów', fontsize='xx-large')
plt.title('Liczba tweetów dotyczących poszczególnych szczepionek', fontsize='xx-large')
plt.ylim(0, 1.1*max(vaccines_count))
ax = plt.gca()
ax.tick_params(axis="x", labelsize=16)
ax.tick_params(axis="y", labelsize=14)
plt.savefig('charts/vaccinesPopularity.png', dpi=200)
plt.close()