from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def overview():
    if request.method == 'POST':
        return "abc" # render_template('hello.html')
    else:
        """We will take all the plots
        """
        return "abcd" #render_template('hello2.html')


"""
HOW TO RUN THE WEB APP ON LOCAL SERVER:
set FLASK_APP=politics.py
python -m flask run

* Running on http://127.0.0.1:5000/
"""
