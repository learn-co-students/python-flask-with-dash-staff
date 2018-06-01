from ourpackage import db

# create models for application
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    tweets = db.relationship('Tweet', backref='users', lazy=True)
    def to_dict(self):
        user = {'id': self.id, 'username': self.username, 'tweets': [tweet.to_dict() for tweet in self.tweets]}
        return user

class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates="tweets")
    def to_dict(self):
        tweet = {'id': self.id, 'text': self.text, 'user_id': self.user.id, 'user': self.user.username}
        return tweet
