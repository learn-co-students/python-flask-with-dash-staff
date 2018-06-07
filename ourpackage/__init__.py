# import Flask
from flask import Flask
# import SQLAlchemy from flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
#import dash
import dash


# initialize new flask app
server = Flask(__name__)
# add configurations and database
server.config['DEBUG'] = True
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tweets.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# connect flask_sqlalchemy to the configured flask app
db = SQLAlchemy(server)
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard')

from ourpackage import routes
