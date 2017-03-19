from flask import Flask
from flask import request
from flask import render_template
from datetime import datetime
import sentiment_analysis_big

import json
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def overview():
    today = datetime.strptime('2017-03-19 18:26:12', '%Y-%m-%d %H:%M:%S') # str(datetime.now())
    # politicians_sent = {"realDonaldTrump":[1.0, 0.5, 0.3, -0.2, -0.5],
    # "BernieSanders":[1.0, 0.5, 0.3, -0.2, -0.5], "HillaryClinton":[1.0, 0.5],
    # "theresa_may":[1.0, 0.5, 0.3, -0.2, -0.5], "NicolaSturgeon":[1.0, 0.5, 0.3, -0.2, -0.5],
    # "tedcruz":[1.0, 0.5, 0.3, -0.2, -0.5], "potus44":[1.0, 0.5, 0.3, -0.2, -0.5],
    # "CoryBooker":[1.0, 0.5, 0.3], "JohnCornyn":[1.0, 0.5, 0.3, -0.2, -0.5],
    # "SenGillibrand":[1.0, 0.5, 0.3, -0.2, -0.5], "SenWarren":[1.0, 0.5, 0.3, -0.2, -0.5],
    # "ChrisMurphyCT":[1.0, 0.5, 0.3, -0.2, -0.5], "SpeakerRyan":[1.0, 0.5, 0.3]}
    if request.method == 'POST':
        # sentiments, dates - both lists, retweets, nick
        return "Not implemented yet."
    else:
        polit_name = "realDonaldTrump" # request.args.get('politician')
        with open('sentiment_weekly_big.json','r') as f:
            sentiment_scores = json.load(f)
        with open('subj_weekly_big.json','r') as f:
            subj_scores = json.load(f)
        with open('sentiment_tweets_big_by_person.json','r') as fl:
            tweets_by_politicians = json.load(fl)
        """For every politician we have a list of tweet details:
         {'date': date, 'name': name, 'num_retweets': retweets, 'sentiment': tweet_t.sentiment.polarity, 'subjectivity': tweet_t.sentiment.subjectivity}
        """
        last_emotions_ranking = sentiment_analysis_big.get_last_emotions_ranking(sentiment_scores)
        last_subj_ranking = sentiment_analysis_big.get_last_subj_ranking(subj_scores)
        similar_people_sent = sentiment_analysis_big.get_similar_people(polit_name, sentiment_scores)
        similar_people_subj = sentiment_analysis_big.get_similar_people_subj(polit_name, subj_scores)

        """What we need?

        The scores for both weekly sentiment and subjectivity for the given
        politician as a list.
        """
        return "qwerty"


        # open the json file and get the data
        # receive nick, send stuff
        return render_template('index.html', today=today, sentiment_scores=sentiment_scores[polit_name], subj_scores=subj_scores[polit_name])


if __name__ == "__main__":
    app.run(host='0.0.0.0')

"""
HOW TO RUN THE WEB APP ON LOCAL SERVER:
python politics.py

* Running on http://127.0.0.1:5000/
"""
