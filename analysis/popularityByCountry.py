import matplotlib.pyplot as plt
import pandas as pd
from common import getDbConn, getCountryNames

def get_tweets_df():
  conn = getDbConn()

  tweet_df = pd.read_sql("select t.tweet_text, p.country_code \
    FROM tweets t \
    left join places p \
    on p.id = t.place_id \
    WHERE t.place_id is not NULL \
    order by 2", conn)
  conn.close()
  return tweet_df

def get_counts_by_country(tweet_df):
  tweet_df.set_index(keys=['country_code'], drop=False,inplace=True)

  # get a list of names
  country_codes=tweet_df['country_code'].unique().tolist()

  counts = {}

  for country_code in country_codes:
      count = len(tweet_df.loc[tweet_df.country_code==country_code])
      # if count > 10:
      #     print(country_code, count)
      #     
      counts[country_code] = count
  counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
  return counts

def save_plot_of_counts(counts):
  country_names = getCountryNames()
  MAX_ITEMS = 20
  counts_keys = list(counts.keys())[:MAX_ITEMS]
  counts_values = list(counts.values())[:MAX_ITEMS]
  counts_keys = [country_names[code] for code in counts_keys]

  rects = plt.bar(counts_keys, counts_values)
  plt.bar_label(rects, rotation=90)
  plt.xticks(rotation=90)
  plt.xlabel('Nazwa kraju')
  plt.ylabel('Liczba tweetów')
  plt.title('Liczba wystąpień tweetów w poszczególnych krajach')
  plt.ylim(0, 1.1*max(counts_values))
  plt.tight_layout()
  plt.savefig('charts/vaccines_popularity_by_country.png')
  plt.close()

tweet_df = get_tweets_df()
counts = get_counts_by_country(tweet_df)
save_plot_of_counts(counts)