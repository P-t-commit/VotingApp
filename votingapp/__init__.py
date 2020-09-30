import pymongo
from pymongo import MongoClient
from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ddab48620ec17904e36d992be1de1ff1'

cluster = pymongo.MongoClient("mongodb+srv://dbAdmin:test@voteapp.u5lp2.mongodb.net/Vote_App?retryWrites=true&w=majority")
# Database = cluster["Vote_App"]

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from votingapp import routes