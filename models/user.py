
from db import db


# must not be the resource, helper class to store some data about the user and auxiliary methods
# Internal Representation
# this is an API, not REST tho, class methods is like an interface
class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))  # String(80) max string length
    password = db.Column(db.String(80))

    # it does not need id because it is auto incrementing (primary key)
    def __init__(self, username, password):
        # Will be used in the database
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
