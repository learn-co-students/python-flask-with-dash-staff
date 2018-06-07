# import Flask
from flask import Flask
# import SQLAlchemy from flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy


# initialize new flask app
app = Flask(__name__)
# add configurations and database
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# connect flask_sqlalchemy to the configured flask app
db = SQLAlchemy(app)

#import our routes after our database has been configured
from ourpackage import routes
