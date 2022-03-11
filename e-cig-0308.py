#!/usr/bin/env python
import pandas as pd
from pmaw import PushshiftAPI
import requests
import json
import csv
import time
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

# get keywords for each Health Category and Symptom from Appendix
keywords = pd.read_csv('keywords.csv',encoding = "ISO-8859-1")
keywords.head()
# convert keywords to dict
keywords_dict = keywords.set_index('Health Category')['Keywords'].to_dict()

# read raw keywords
my_file = open("subreddit-list.txt", "r")
content = my_file.read()
content_list = content.split(",")
my_file.close()

# read string list to new list
subreddit_list = []
for name in content_list:
    name = name.strip()
    if name not in subreddit_list:
        subreddit_list.append(name)

# query from Reddit
api = PushshiftAPI()

before = int(datetime(2019,4,30,0,0).timestamp())
after = int(datetime(2013,1,1,0,0).timestamp())

# subreddit = 'marijuana'
q_list = ['respiratory','cardiovascular','neurological','psychological','digestive','mouth','throat','cancer']
q = 'cancer' # q = '*' for everything
for subreddit in subreddit_list[6::]:
    for item in keywords_dict:
        sub_words = keywords_dict[item].split(', ')
        posts_sum = pd.DataFrame()
        comments_sum = pd.DataFrame()
        # start reddit query
        for q in sub_words:
            try:
                limit=100000
                posts = api.search_submissions(subreddit=subreddit, q=q, limit=limit, before=before, after=after)
                comments = api.search_comments(subreddit=subreddit, q=q, limit=limit, before=before, after=after)
                print(f'Retrieved {len(posts)} posts from Pushshift')
                print(f'Retrieved {len(comments)} comments from Pushshift')

                posts_df = pd.DataFrame(posts)
                comments_df = pd.DataFrame(comments)

                # print(posts_df.head())
                # remove null created_utc rows
                posts_df = posts_df.loc[posts_df.created_utc.notnull()]
                comments_df = comments_df.loc[comments_df.created_utc.notnull()]
                # create datetime
                posts_df['created_datetime'] = [datetime.fromtimestamp(x) for x in posts_df.created_utc]
                comments_df['created_datetime'] = [datetime.fromtimestamp(x) for x in comments_df.created_utc]

                # add Health Category and Symptom into dataframe
                posts_df['Health Category'] = item
                posts_df['Health Symptom'] = q
                comments_df['Health Category'] = item
                comments_df['Health Symptom'] = q

                # merge dataframe
                try:
                    posts_sum = posts_sum.append(posts_df, sort=False)
                    comments_sum = comments_sum.append(comments_df, sort=False)
                except:
                    print('missing dataframe columns')

            except:
                print('No Posts about {} in {}'.format(q, item))

        # save to csv
        posts_sum.to_csv('data/{}_posts_{}.csv'.format(subreddit, item), header=True, index=False)
        comments_sum.to_csv('data/{}_comments_{}.csv'.format(subreddit, item), header=True, index=False)

        print('Download {} related posts and comments from subreddit {}'.format(item, subreddit))


