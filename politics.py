from flask import Flask
from flask import request
from flask import render_template
from datetime import datetime
import sentiment_analysis_big
from flask import jsonify

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
    politicians_dct = {"realDonaldTrump": "Donald J. Trump", "BernieSanders": "Bernie Sanders",
    "HillaryClinton": "Hillary Clinton", "theresa_may": "Theresa May",
    "NicolaSturgeon": "Nicola Sturgeon", "tedcruz": "Ted Cruz", "potus44": "Barack Obama",
    "CoryBooker": "Cory Booker", "JohnCornyn": "John Cornyn", "SenGillibrand": "Kirsten Gillibrand",
    "SenWarren": "Elizabeth Warren", "ChrisMurphyCT": "Chris Murphy", "SpeakerRyan": "Paul Ryan"}
    if request.method == 'POST':
        # sentiments, dates - both lists, retweets, nick
        return "We do not use post requests currently."
    else:
        try:
            polit_name = request.args.get('politician')
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
            changes_em = sentiment_analysis_big.get_people_biggest_change(sentiment_scores)
            changes_subj = sentiment_analysis_big.get_people_biggest_change(subj_scores)
            """What we need?

            The scores for both weekly sentiment and subjectivity for the given
            politician as a list.
            """
            # return "qwerty"
            top3sent = list(map(lambda x: [x[1], x[2]], similar_people_sent[1:4]))
            """top3sent is a list of tuples containing (name, similarity) each
            the same for top3subj.
            """
            top3subj = list(map(lambda x: [x[1], x[2]], similar_people_subj[1:4]))


            # open the json file and get the data
            # receive nick, send stuff
            # pass also data for the most similar politicians
            return jsonify(
                           today=today,
                           politicians_dct=politicians_dct,
                           top3sent=top3sent,
                           top3subj=top3subj,
                           sentiment_scores=sentiment_scores[polit_name],
                           subj_scores=subj_scores[polit_name],
                           tweets_by_politician=tweets_by_politicians[polit_name]
                          )
            # return render_template('index.html', )
        except:
            """
            Interesting information to use: both for sent and subj
            top5posit
            top5neg
            top5posrise
            top5negdec
            """
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
            changes_em = sentiment_analysis_big.get_people_biggest_change(sentiment_scores)
            changes_subj = sentiment_analysis_big.get_people_biggest_change(subj_scores)
            top5posit_sent = last_emotions_ranking[:5]
            top5neg_sent = last_emotions_ranking[-5:]
            top5posrise_sent = changes_em[:5]
            top5negdec_sent = changes_em[-5:]
            top5posit_subj = last_subj_ranking[:5]
            top5neg_subj = last_subj_ranking[-5:]
            top5posrise_subj = changes_subj[:5]
            top5negdec_subj = changes_subj[-5:]
            return jsonify(
                           politicians_dct=politicians_dct,
                           top5posit_sent = top5posit_sent,
                           top5neg_sent = top5neg_sent,
                           top5posrise_sent = top5posrise_sent,
                           top5negdec_sent = top5negdec_sent,
                           top5posit_subj = top5posit_subj,
                           top5neg_subj = top5neg_subj,
                           top5posrise_subj = top5posrise_subj,
                           top5negdec_subj = top5negdec_subj
                          )

if __name__ == "__main__":
    app.run(host='0.0.0.0')

"""
HOW TO RUN THE WEB APP ON LOCAL SERVER:
python politics.py

* Running on http://127.0.0.1:5000/
"""
