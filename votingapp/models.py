from votingapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader 
def load_user(user_id):
    try:
        print("i am here")
        return User.query.get(int(user_id))
    except Exception as e:
        print("try was unsuccessful")
        print(e)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    #username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(200), unique=True, nullable = False)
    # password = db.Column(db.String(60), nullable = False)
    hasVoted = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"User('{self.email}')"
        # return f"User('{self.username}', '{self.email}')"

    def __init__(self, email):
        # self.username = username
        # self.password = password
        self.email = email

    # def __init__(self, username, password, email):
    #     self.username = username
    #     self.password = password
    #     self.email = email

class Votes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    candidate_name = db.Column(db.String(20), unique=True, nullable=False)
    votes = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, candidate_name):
        self.candidate_name = candidate_name

    def __repr__(self):
        return f"CandidateVotes('{self.candidate_name}', '{self.votes}')"
