from src.common.database import Database
from flask import session
import uuid
from src.models.blog import Blog

__author__ = "hmorrin"

class User(object):
    """docstring forUser."""

    def __init__(self,email,password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email" : email })
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls,id):
        data = Database.find_one("users", {"id" : id })
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email,password):
        #Check whether a users email matches the password they sent us
        user=User.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls,email,password):
        user=cls.get_by_email(email)
        if user is None:
            new_user = cls(email,password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        #login valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        #login valid has already been called
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def json(self):
        return {
            "email" : self.email,
            "_id" : self._id,
            "password" : self.password
        }


    def save_to_mongo(self):
        Database.insert("users", self.json())
