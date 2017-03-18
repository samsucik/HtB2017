import tweepy
import key

auth = tweepy.OAuthHandler(key.consumer_key, 	key.consumer_secret)
auth.set_access_token(key.access_token, 	key.access_token_secret)

api = tweepy.API(auth)


def get_tweets(user):
    return api.user_timeline(user)

public_tweets = get_tweets("Google")
for tweet in public_tweets:
    print(tweet.text)
