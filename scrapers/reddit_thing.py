import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')

from django.db import models
from news.models import *
from datetime import datetime
import traceback
import praw
import datetime
import time


r = praw.Reddit(user_agent="data_science_project")
subreddit = r.get_subreddit('news') #Right now, its just getting from /r/news. We could either do all the same steps below, also with /r/worldnews, OR, do news+worldnews to do both at the same time. 
for submission in subreddit.get_hot(limit=30): #May want to change limit=1 to something higher. The max for a single call to the server is 200 (i think).
	post_score =  submission.score
	post_title = submission.title
	post_url = submission.url #Sometimes this just links to an image, or reddit post. It's not always an article.
	#We'll have to turn this into an actual date. Looking at some other scripts, it looks like someone has already figured out how to do that. If not, I can work on it later, just let me know.
	post_created_at = datetime.datetime(*time.localtime(submission.created_utc)[:6])


	forest_of_comments = submission.comments
        comments = []
	for x in xrange(min(len(forest_of_comments), 30)): # Just getting the top ten comments for now. This also assumes that there are at least 10 comments (which I think will always be true for the top articles)
                comment = forest_of_comments[x]
		comment_text = comment.body
		comment_score = comment.score
		
		#Similar thing here. Time needs to be converted to actual date.
		comment_date = datetime.datetime(*time.localtime(comment.created_utc)[:6])
                comments.append({
                    'text' : comment_text,
                    'creation_time' : comment_date
                })
        
        data = {
            'url' : post_url,
            'subreddit' : 'news',
            'post_title' : post_title,
            'votes' : post_score,
            'submission_time' : post_created_at 
        }
        try:
            reddit_post(data, comments)
        except Exception as ex:
            print traceback.format_exc()
            print 'reddit post could not be created'
            print ex
