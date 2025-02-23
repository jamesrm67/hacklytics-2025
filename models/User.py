from flask_login import UserMixin
from firebase_admin import auth

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email
    
    def get_id(self):
        return str(self.id)

def get_user(user_id):
    try:
        user = auth.get_user(user_id)
        return User(user.id, user.username, user.email)
    except auth.UserNotFoundError:
        return None
    except Exception as e:
        return None