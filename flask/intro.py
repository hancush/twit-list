from flask import Flask, render_template, redirect, session

import tweepy

import topper as t
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
    lists = t.get_lists(session['user']) # 15 per 15 min
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
    sample = t.get_tweets(session['which'], int(session['hours']))
    results = t.score_tweets(sample)
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
