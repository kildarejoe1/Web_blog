__author__ = "hmorrin"
import datetime
import uuid
from src.models.post import Post
from src.common.database import Database


class Blog(object):
    """docstring for Blog."""

    def __init__(self, author, title,description,author_id,_id=None,):
        self.author=author
        self.author_id = author_id
        self.title=title
        self.description=description
        self._id=uuid.uuid4().hex if _id is None else _id


    def new_post(self):
        title = str(raw_input("Enter post title:"))
        content = str(raw_input("Enter post content: "))
        date = str(raw_input("Enter post date, or leave blank for the dare ( in format DDMMYYY):"))
        if date == "":
            date=datetime.datetime.utcnow()
        else:
            date=datetime.datetime.strptime(date,"%d%m%y")
        post = Post(blog_id=self._id, title=title,content=content,author=self.author, date= date)
        post.save_to_mongo()



    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return { '_id' : self._id,
                 'author' : self.author,
                 'author_id': self.author_id,
                 'title' : self.title,
                 'description' : self.description
                 }
    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': id})
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection='blogs',
                              query={'author_id': author_id})
        return [cls(**blog) for blog in blogs]
