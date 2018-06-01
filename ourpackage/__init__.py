# import requests module to make http requests
import requests
# import Flask, jsonify, render_template, and json from flask
from flask import Flask
# import SQLAlchemy from flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
#import dash
import dash


# initialize new flask app
server = Flask(__name__)
# add configurations and database
server.config['DEBUG'] = True
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# connect flask_sqlalchemy to the configured flask app
db = SQLAlchemy(server)
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard')

from ourpackage import routes
