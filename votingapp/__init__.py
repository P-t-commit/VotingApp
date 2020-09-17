from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from LoginRadius import LoginRadius as LR


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ddab48620ec17904e36d992be1de1ff1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACKS_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# LR.API_KEY = "e91795bb-fa16-40b6-b9bd-1d8f120333de"
# LR.API_SECRET = "e19e43cc-7ebe-42a1-999d-f3a271d12bd8"
# loginradius = LR()

# LR.API_REQUEST_SIGNING = True

from votingapp import routes