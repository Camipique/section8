# User object class
# id is a python keyword, so _id
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    # Makes part of the Item class
    parser = reqparse.RequestParser()
    # add info to parse the arguments, type, required or not, help if something wrong, etc...
    parser.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

    def post(self):
        # if there is more arguments it doesn't matter
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "A user with that username already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201  # 201 is for created
