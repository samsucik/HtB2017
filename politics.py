from flask import Flask
app = Flask(__name__)

@app.route('/')
def overview():
    return 'The most sentimental politician this week: Donald Trump'

"""
HOW TO RUN THE WEB APP ON LOCAL SERVER:
set FLASK_APP=politics.py
python -m flask run

* Running on http://127.0.0.1:5000/
"""
