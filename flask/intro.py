from flask import Flask, render_template, redirect, session

import tweepy

from topper_class import Rank
from form_class import Intro, ListDrop

app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods=['GET', 'POST'])
def get_user():
    pageType = 'intro'
    form = Intro()
    if form.is_submitted():
        user = form.user.data
        session['user'] = user
        return redirect('/lists')
    return render_template('app.html',
                           pageType=pageType,
                           form=form)

@app.route('/lists', methods=['GET', 'POST'])
def lists():
    pageType = 'lists'
    go = Rank()
    lists = go.get_lists(session['user']) # 15 per 15 min
    form2 = ListDrop()
    form2.which.choices = lists
    if form2.is_submitted():
        which = form2.which.data
        session['which'] = which
        hours = form2.hours.data
        session['hours'] = hours
        return redirect('/results')
    return render_template('app.html',
                           form2=form2,
                           pageType=pageType)

@app.route('/results', methods=['GET'])
def results():
    pageType = 'results'
    go = Rank()
    tweets = go.get_tweets(int(session['which']))
    sample = go.sample_per(tweets, int(session['hours']))
    results = go.score(sample)
    return render_template('app.html',
                       pageType=pageType,
                       results=results,
                       hours=session['hours'])

@app.errorhandler(tweepy.TweepError)
def rate_limit_exceeded(e):
    return render_template('app.html',
                       pageType='error')


if __name__ == '__main__':
    app.run(debug=True)
