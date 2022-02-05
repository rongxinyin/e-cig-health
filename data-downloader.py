import pandas as pd
from pmaw import PushshiftAPI
import requests
import json
import csv
import time
from datetime import datetime, timedelta

api = PushshiftAPI()

before = int(datetime(2021,12,31,0,0).timestamp())
after = int(datetime(2013,1,1,0,0).timestamp())

subreddit = 'marijuana'
q_list = ['respiratory','cardiovascular','neurological','psychological','digestive','mouth','throat','cancer']
q = 'cancer' # q = '*' for everything
for q in q_list:
	limit=100000
	posts = api.search_submissions(subreddit=subreddit, q=q, limit=limit, before=before, after=after)
	comments = api.search_comments(subreddit=subreddit, q=q, limit=limit, before=before, after=after)
	print(f'Retrieved {len(posts)} posts from Pushshift')
	print(f'Retrieved {len(comments)} comments from Pushshift')

	posts_df = pd.DataFrame(posts)
	comments_df = pd.DataFrame(comments)

	# print(posts_df.head())
	# preview the comments data
	posts_df['created_datetime'] = [datetime.fromtimestamp(x) for x in posts_df.created_utc]
	comments_df['created_datetime'] = [datetime.fromtimestamp(x) for x in comments_df.created_utc]

	# save to csv
	posts_df.to_csv('data/mari_posts_{}.csv'.format(q), header=True, index=False, columns=list(posts_df.axes[1]))
	comments_df.to_csv('data/mari_comments_{}.csv'.format(q), header=True, index=False, columns=list(comments_df.axes[1]))

	print('Download {} related posts and comments'.format(q))