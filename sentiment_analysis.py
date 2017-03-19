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
                record = {'date': str(date)[:-1], 'name': str(name)[:-1], 'num_retweets': retweets, 'tweet': str(line)[:-1], 'sentiment': tweet_t.sentiment.polarity}
                records.append(record)
                # now save it to a database
    # sent = []
    # zeros = 0
    # for e in records:
    #      sent.append(e['sentiment'])
    # for e in sent:
    #     if e==0.0:
    #         zeros += 1
    # print(zeros*1.0/len(records))
    with open('sentiment_tweets.json','w') as f:
        json.dump(records, f)

    # print(records)
    # list_people = ["realdonaldtrump", "hillaryclinton"]
    # text = "My representatives had a great meeting w/ the Hispanic Chamber of Commerce at the WH today. Look forward to tremendous growth & future mtgs!"
    # a = TextBlob(text)
    # a.sentiment.polarity

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
        num_weeks = 1 + ((today - datetime.strptime(tweets_by_politicians[polit][-1]['date'], '%Y-%m-%d %H:%M:%S')).days) // 7
        polit_weekly_scores[polit] = []
        polit_weekly_tweets[polit] = [[] for i in range(num_weeks)]
        for tweet in tweets_by_politicians[polit]:
            polit_weekly_tweets[polit][((today - datetime.strptime(tweet['date'], '%Y-%m-%d %H:%M:%S')).days) // 7].append(tweet)
    for polit in polit_weekly_scores:
        for week in polit_weekly_tweets[polit]:
            scores = []
            for item in week:
                scores.append(item['sentiment'])
            if len(scores)==0:
                polit_weekly_scores[polit].append(0)
            else:
                polit_weekly_scores[polit].append(mean(scores))
    print(polit_weekly_scores)
    with open('sentiment_weekly.json','w') as f:
        json.dump(polit_weekly_scores, f)
    return(polit_weekly_scores)
