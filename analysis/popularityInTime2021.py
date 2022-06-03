import matplotlib.pyplot as plt
from common import getDbCursor, vaccines_dict

myCursor = getDbCursor()

def plotInTime(vaccine_name):
    myCursor.execute(f"select cast(created_at as DATE) date, count(*) from tweets where lower(tweet_text) like '%{vaccine_name}%' and created_at between '2021-01-01 00:00:00' and '2021-02-21 00:00:00' group by date")
    astra = myCursor.fetchall()
    data = []
    dates = []
    for x in astra:
        data.append(x[1])
        dates.append(x[0])

    vaccine = vaccines_dict[vaccine_name]
    print('Plotting', vaccine['display_name'])
    plt.plot(dates, data, vaccine['color'] + 'o--', label=vaccine['display_name'])
    return dates[::20]

plt.figure(figsize=(24,10))

dates = None
for vaccine_name in vaccines_dict.keys():
    dates = plotInTime(vaccine_name)
plt.xticks(dates)

plt.ylabel('Liczba tweetów', fontsize='xx-large')
plt.xlabel('Data', fontsize='xx-large')
plt.title('Liczba tweetów dotyczących poszczególnych szczepionek dla 2021 roku', fontsize='xx-large')
plt.legend(fontsize='xx-large')
ax = plt.gca()
ax.tick_params(axis="x", labelsize=16, labelrotation=90)
ax.tick_params(axis="y", labelsize=14)
plt.tight_layout()
plt.savefig('charts/vaccinesPopularityInTime2021.png', dpi=200)
plt.close()