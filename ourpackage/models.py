from ourpackage import db

# created models for application
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


# created and seeded tables
db.create_all()

daniel = User(username="Daniel")
jeff = User(username="Jeff")
rachel = User(username="Rachel")

daniel.tweets = [Tweet(text="I love hogs"), Tweet(text="Hogs are the best way to teach react"), Tweet(text="Programming is lyfe")]
jeff.tweets = [Tweet(text="Data Science is awesome"), Tweet(text="Python is pretty neat"), Tweet(text="Wishing I was chillin' in mexico rn")]
rachel.tweets = [Tweet(text="RPDR is the best show"), Tweet(text="I just made the coolest NPM package!"), Tweet(text="Running is so fun!")]

if db.session.query(User).all() == []:
    db.session.add(jeff)
    db.session.add(rachel)
    db.session.add(daniel)
    db.session.commit()
