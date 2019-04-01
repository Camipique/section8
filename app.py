from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

# JWT stands for JSON Web Token
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# Resource is something that the API represents/returns
app = Flask(__name__)

# Will live in the root folder of our project, we can also use postsql, oracle, etc instead of sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'jose'

# Easily add resources
api = Api(app)

# creates endpoint /auth, we send user_name and pw, client sending jwt will know
# what user is authenticated
jwt = JWT(app, authenticate, identity)

# This resource, will be access via API
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')
# We will run this only if we do python app.py this is __main__, if not it means it was imported
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
