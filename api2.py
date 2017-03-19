import tweepy #https://github.com/tweepy/tweepy
import csv
import wget
import key

#Twitter API credentials
consumer_key = key.consumer_key
consumer_secret = key.consumer_secret
access_key = key.access_token
access_secret = key.access_token_secret


def get_all_tweets(screen_name):
	
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	

	#Download the user's image
	save_picture(new_tweets[0], screen_name)

	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before {0}".format(oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("...%s tweets downloaded so far {0}".format(len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.retweet_count, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","retweet_count","text"])
		writer.writerows(outtweets)
	
	pass

def save_picture(tweet, screen_name):
	img = tweet.user.profile_image_url.replace('_normal', '_400x400')
	wget.download(img, ("static/" + tweet.user.screen_name + ".jpg").lower())



if __name__ == '__main__':
	#pass in the username of the account you want to download
    politicians = ["realDonaldTrump","TotalBiscuit","BernieSanders","HillaryClinton","theresa_may", "NicolaSturgeon","tedcruz","potus44", "CoryBooker","JohnCornyn","SenGillibrand", "SenWarren","ChrisMurphyCT", "SpeakerRyan"]
    for politician in politicians:
        get_all_tweets(politician)
