import praw
r = praw.Reddit(user_agent="lol_stuff")
subreddit = r.get_subreddit('news')
for submission in subreddit.get_hot(limit=1): #May want to change limit=1 to something higher. The max for a single call to the server is 200 (i think).
	post_score =  submission.score
	post_title = submission.title
	post_url = submission.url #Sometimes this just links to an image, or reddit post. It's not always an article.
	#We'll have to turn this into an actual date. Looking at some other scripts, it looks like someone has already figured out how to do that. If not, I can work on it later, just let me know.
	post_created_at = submission.created 
	post_created_at = submission.created_utc	


	forest_of_comments = submission.comments
	for x in range(0, 10): # Just getting the top ten comments for now. This also assumes that there are at least 10 comments (which I think will always be true for the top articles)
		comment = forest_of_comments[x]

		comment_text = comment.body
		comment_score = comment.score
		
		#Similar thing here. Time needs to be converted to actual date.
		comment.created
		comment.created_utc
