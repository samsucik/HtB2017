from textblob import TextBlob
import json
from datetime import datetime, timedelta
from statistics import mean

def create_json():
    with open('file.txt', 'r', encoding='utf-8') as f:
        it = 0
        record = {}
        records = []
        for line in f:
            if it==0:
                it = 1
                date = line
            elif it==1:
                it = 2
                name = line
                # politician's name
            elif it==2:
                it = 3
                # tweet itself
                tweet = line
            else:
                it = 0
                retweets = int(line)
                tweet_t = TextBlob(tweet)
                record = {'date': str(date)[:-1], 'name': str(name)[:-1], 'num_retweets': retweets, 'tweet': str(line)[:-1], 'sentiment': tweet_t.sentiment.polarity, 'subjectivity': tweet_t.sentiment.subjectivity}
                records.append(record)

    with open('sentiment_tweets.json','w') as f:
        json.dump(records, f)

def get_weekly_sentiments():
    """The output is a dictionary with keys the names of the politicians
    and values list of their average weekly sentiments arranged from the latest data to the oldest.
    """
    politicians = ["realDonaldTrump", "BernieSanders", "HillaryClinton", "theresa_may",
    "NicolaSturgeon", "tedcruz", "potus44", "CoryBooker", "JohnCornyn", "SenGillibrand", "SenWarren",
    "ChrisMurphyCT", "SpeakerRyan"]

    with open('sentiment_tweets.json','r') as f:
        records = json.load(f)
    """
    Convert string time to an object Datetime
    from datetime import datetime, timedelta
    datetime_object = datetime.strptime('2017-03-17 12:26:12', '%Y-%m-%d %H:%M:%S')
    timedelta(days=7)
    """
    week_length = 3
    tweets_by_politicians = {}
    polit_weekly_tweets = {}
    polit_weekly_scores = {}
    for record in records:
        if record['name'] not in tweets_by_politicians:
            tweets_by_politicians[record['name']] = []
            polit_weekly_scores[record['name']] = []
            polit_weekly_tweets[record['name']] = []
        tweets_by_politicians[record['name']].append(record)
    for politician in tweets_by_politicians:
        tweets_by_politicians[politician].sort(key=lambda x: x['date'], reverse=True)
    for politician in tweets_by_politicians:
        tweets_by_politicians[politician].sort(key=lambda x: x['date'], reverse=True)
    for polit in polit_weekly_tweets:
        # the next will be changed later to something better
        today = datetime.strptime('2017-03-19 18:26:12', '%Y-%m-%d %H:%M:%S')
        num_weeks = 1 + ((today - datetime.strptime(tweets_by_politicians[polit][-1]['date'], '%Y-%m-%d %H:%M:%S')).days) // week_length
        polit_weekly_scores[polit] = []
        polit_weekly_tweets[polit] = [[] for i in range(num_weeks)]
        for tweet in tweets_by_politicians[polit]:
            polit_weekly_tweets[polit][((today - datetime.strptime(tweet['date'], '%Y-%m-%d %H:%M:%S')).days) // week_length].append(tweet)
    for polit in polit_weekly_scores:
        for week in polit_weekly_tweets[polit]:
            scores = []
            for item in week:
                scores.append(item['sentiment'])
            if len(scores)==0:
                polit_weekly_scores[polit].append(0)
            else:
                polit_weekly_scores[polit].append(mean(scores))
    print("Weekly sentiment scores:")
    # from -1 to 1
    print(polit_weekly_scores)
    with open('sentiment_weekly.json','w') as f:
        json.dump(polit_weekly_scores, f)
    return(polit_weekly_scores)

def get_weekly_subjectivity():
    """The output is a dictionary with keys the names of the politicians
    and values list of their average weekly subjectivity arranged from the latest data to the oldest.
    """
    politicians = ["realDonaldTrump", "BernieSanders", "HillaryClinton", "theresa_may",
    "NicolaSturgeon", "tedcruz", "potus44", "CoryBooker", "JohnCornyn", "SenGillibrand", "SenWarren",
    "ChrisMurphyCT", "SpeakerRyan"]

    with open('sentiment_tweets.json','r') as f:
        records = json.load(f)
    """
    Convert string time to an object Datetime
    from datetime import datetime, timedelta
    datetime_object = datetime.strptime('2017-03-17 12:26:12', '%Y-%m-%d %H:%M:%S')
    timedelta(days=7)
    """
    week_length = 3
    tweets_by_politicians = {}
    polit_weekly_tweets = {}
    polit_weekly_scores = {}
    for record in records:
        if record['name'] not in tweets_by_politicians:
            tweets_by_politicians[record['name']] = []
            polit_weekly_scores[record['name']] = []
            polit_weekly_tweets[record['name']] = []
        tweets_by_politicians[record['name']].append(record)
    for politician in tweets_by_politicians:
        tweets_by_politicians[politician].sort(key=lambda x: x['date'], reverse=True)
    for politician in tweets_by_politicians:
        tweets_by_politicians[politician].sort(key=lambda x: x['date'], reverse=True)
    for polit in polit_weekly_tweets:
        # the next will be changed later to something better
        today = datetime.strptime('2017-03-19 18:26:12', '%Y-%m-%d %H:%M:%S')
        num_weeks = 1 + ((today - datetime.strptime(tweets_by_politicians[polit][-1]['date'], '%Y-%m-%d %H:%M:%S')).days) // week_length
        polit_weekly_scores[polit] = []
        polit_weekly_tweets[polit] = [[] for i in range(num_weeks)]
        for tweet in tweets_by_politicians[polit]:
            polit_weekly_tweets[polit][((today - datetime.strptime(tweet['date'], '%Y-%m-%d %H:%M:%S')).days) // week_length].append(tweet)
    for polit in polit_weekly_scores:
        for week in polit_weekly_tweets[polit]:
            scores = []
            for item in week:
                scores.append(item['subjectivity'])
            if len(scores)==0:
                polit_weekly_scores[polit].append(0.5)
            else:
                polit_weekly_scores[polit].append(mean(scores))
    print("Weekly subjectivity scores:")
    # from 0 (very objective) to 1 (very subjective)
    print(polit_weekly_scores)
    with open('subj_weekly.json','w') as f:
        json.dump(polit_weekly_scores, f)
    return(polit_weekly_scores)

def get_similar_people(politician, polit_weekly_scores):
    """Find politicians with a similar evolution of emotions in twitter messages
    over past two weeks to a given politician."""
    polit_last_two_scores = polit_weekly_scores[politician][:2]
    last_scores = []
    for name in polit_weekly_scores:
        last_scores.append((name, polit_weekly_scores[name][:2]))
    distances = [(((i[1][0]-polit_last_two_scores[0])**2 + (i[1][1]-polit_last_two_scores[1])**2)**0.5, i[0]) for i in last_scores]
    distances.sort(key=lambda x: x[0])
    similar = map(lambda x: (x[0], x[1], 1.0/(1.0+x[0])), distances)
    return list(similar)

def get_similar_people_subj(politician, polit_weekly_scores):
    """Find politicians with a similar evolution of subjectivity in twitter messages
    over past two weeks to a given politician."""
    polit_last_two_scores = polit_weekly_scores[politician][:2]
    last_scores = []
    for name in polit_weekly_scores:
        last_scores.append((name, polit_weekly_scores[name][:2]))
    distances = [(((i[1][0]-polit_last_two_scores[0])**2 + (i[1][1]-polit_last_two_scores[1])**2)**0.5, i[0]) for i in last_scores]
    distances.sort(key=lambda x: x[0])
    similar = map(lambda x: (x[0], x[1], 1.0/(1.0+x[0])), distances)
    return list(similar)

def get_last_emotions_ranking(polit_weekly_scores):
    """Get a ranking of politicians based on being the most negative in a given week"""
    last_scores = []
    for name in polit_weekly_scores:
        last_scores.append((name, polit_weekly_scores[name][0]))
    last_scores.sort(key=lambda x: x[1])
    return last_scores

def get_last_subj_ranking(polit_weekly_scores):
    """Get a ranking of politicians based on being the most negative in a given week"""
    last_scores = []
    for name in polit_weekly_scores:
        last_scores.append((name, polit_weekly_scores[name][0]))
    last_scores.sort(key=lambda x: x[1])
    return last_scores

a = get_weekly_sentiments()
b = get_weekly_subjectivity()
print("Emotions/sentiment ranking")
print(get_last_emotions_ranking(a))
print("Subjectivity ranking:")
print(get_last_subj_ranking(b))
print("Most similar people to Donald Trump in terms of emotions:")
print(get_similar_people('Donald J. Trump', a))
print("Most similar people to Donald Trump in terms of subjectivity:")
print(get_similar_people('Donald J. Trump', b))
