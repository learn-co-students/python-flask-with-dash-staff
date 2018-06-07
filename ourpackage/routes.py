from flask import render_template, jsonify, json
from ourpackage.models import User, Tweet, db
# from ourpackage import db, app
from ourpackage.dashboard import app

#define a second route to display our dashboard
@app.server.route('/go-to-dashboard')
def dashboard():
    return app.index()

# created JSON routes for our API
@app.server.route('/api/users')
def user_index():
    all_users = db.session.query(User).all()
    all_users_dicts = [user.to_dict() for user in all_users]
    return jsonify(all_users_dicts)

@app.server.route('/api/users/<int:id>')
def find_user(id):
    user = User.query.filter(User.id == id).first()
    return jsonify(user.to_dict())

@app.server.route('/api/users/<name>')
def find_user_by_name(name):
    user = User.query.filter(User.username.like(name)).first()
    return jsonify(user.to_dict())

@app.server.route('/api/tweets')
def tweet_index():
    all_tweets = Tweet.query.all()
    all_tweets_dicts = [tweet.to_dict() for tweet in all_tweets]
    return jsonify(all_tweets_dicts)

@app.server.route('/api/tweets/<int:id>')
def find_tweet(id):
    return jsonify(Tweet.query.filter(Tweet.id == id).first().to_dict())

@app.server.route('/api/users/<int:user_id>/tweets')
def find_users_tweets(user_id):
    return jsonify(User.query.filter(User.id == user_id).first().to_dict())

@app.server.route('/api/users/<user_name>/tweets')
def find_users_tweets_by_user_name(user_name):
    return jsonify(User.query.filter(User.name == user_name.lower().title()).first().tweets())

@app.server.route('/api/tweets/<int:tweet_id>/user')
def find_tweets_user(tweet_id):
    return jsonify(Tweet.query.filter(Tweet.id == tweet_id).first().user.to_dict())


# created routes for the appropriate HTML Templates
@app.server.route('/users')
def users_index():
    all_users = db.session.query(User).all()
    all_users_dicts = [user.to_dict() for user in all_users]
    return render_template('users.html', users=all_users_dicts)

@app.server.route('/users/<int:id>')
def user_show_by_id(id):
    user = User.query.filter(User.id == id).first().to_dict()
    return render_template('user_show.html', user=user)

@app.server.route('/users/<name>')
def user_show_by_name(name):
    user = User.query.filter(User.username.like(name)).first().to_dict()
    return render_template('user_show.html', user=user)

@app.server.route('/tweets')
def tweets_index():
    all_tweets = Tweet.query.all()
    all_tweets_dicts = [tweet.to_dict() for tweet in all_tweets]
    return render_template('tweets.html', tweets=all_tweets_dicts)

@app.server.route('/tweets/<int:id>')
def tweet_show_by_id(id):
    tweet = Tweet.query.filter(Tweet.id == id).first().to_dict()
    return render_template('tweet_show.html', tweet=tweet)

@app.server.route('/users/<int:user_id>/tweets')
def find_tweets_by_user_id(user_id):
    user_tweets = User.query.filter(User.id == user_id).first().to_dict()
    return render_template('tweets.html', tweets=user_tweets['tweets'])

@app.server.route('/users/<user_name>/tweets')
def find_tweets_by_username(user_name):
    user_tweets = User.query.filter(User.username == user_name.lower().title()).first().to_dict()
    return render_template('tweets.html', tweets=user_tweets['tweets'])

@app.server.route('/tweets/<int:tweet_id>/user')
def find_user_by_tweet(tweet_id):
    tweet = Tweet.query.filter(Tweet.id == tweet_id).first().to_dict()
    user = User.query.filter(User.id == tweet['user_id']).first().to_dict()
    return render_template('user_show.html', user=user)
