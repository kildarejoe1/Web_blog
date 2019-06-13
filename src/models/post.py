__author__ = "hmorrin"
from src.common.database import Database
import uuid
import datetime



class Post(object):

    def __init__(self,blog_id, title, content, author, date = datetime.datetime.utcnow(), id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.id= uuid.uuid4().hex if id is None else id
        self.created_date = date

    def save_to_mongo(self):
        Database.insert(collection='posts', data=self.json())
#This method used to send object data(attributes) to database as dictionary object
    def json(self):
        return { 'id' : self.id,
                 'blog_id' : self.blog_id,
                 'author' : self.author,
                 'content' : self.content,
                 'title' : self.title,
                 'created_date' : self.created_date
                 }

    @staticmethod
    def from_mongo(id):
        return  Database.find_one(collection="posts", query={'id' : id})

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection="posts", query={'blog_id' : id})]
