def get_sentiment():
	afinnfile = open("/course/cs1951a/pub/assignment3/data/AFINN-111.txt")
	for line in afinnfile:
		term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
		sentiment_scores[term] = float(score)      # Convert the score to a float.
		

def main():
	global sentiment_scores
	sentiment_scores = {}
	
	get_sentiment()

if __name__ == "__main__":
    main()