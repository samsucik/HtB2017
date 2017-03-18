import tweepy
import key

auth = tweepy.OAuthHandler(key.consumer_key, 	key.consumer_secret)
auth.set_access_token(key.access_token, 	key.access_token_secret)

api = tweepy.API(auth)


def get_tweets(user):
    return api.user_timeline(user, count = 150)

def print_user_tweets(user):
    with open('file.txt', 'a', encoding='utf-8') as file:
        for tweet in get_tweets(user):
            print(tweet.retweet_count)
            file.write('{0}\n{1}\n{2}\n{3}\n'.format(str(tweet.created_at), tweet.author.name, str(tweet.text).replace("\n"," "), tweet.retweet_count))


with open('file.txt', 'w') as file:
    print("Wiping file")

print_user_tweets("realDonaldTrump")
print_user_tweets("BernieSanders")
print_user_tweets("HillaryClinton")
print_user_tweets("theresa_may")
print_user_tweets("NicolaSturgeon")
print_user_tweets("tedcruz")
print_user_tweets("potus44")
print_user_tweets("CoryBooker")
print_user_tweets("JohnCornyn")
print_user_tweets("SenGillibrand")
print_user_tweets("SenWarren")
print_user_tweets("ChrisMurphyCT")
print_user_tweets("SpeakerRyan")