from votingapp import login_manager, cluster
from flask_login import UserMixin
import uuid

@login_manager.user_loader
def load_user(user_id):
    my_user = User.get_by_id(user_id)
    if my_user is not None:
        return my_user
    else:
        return None


class User(UserMixin):
    
    def __init__(self, email, hasVoted, _id):
        self.email = email
        self.hasVoted = hasVoted
        self._id = _id

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return self._id

    @classmethod
    def get_by_email(cls,email):
        db = cluster["Vote_App"]
        Database = db["User"]
        data = Database.find_one({"email" : email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls,_id):
        db = cluster["Vote_App"]
        Database = db["User"]
        data = Database.find_one({"_id" : _id})
        if data is not None:
            return cls(**data)


