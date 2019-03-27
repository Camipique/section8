from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


# Every resource has to be a class (Item is a copy of Resource class, with some changes)
# Resources will only have get, post, delete, put..
class Item(Resource):
    # Makes part of the Item class
    parser = reqparse.RequestParser()
    # add info to parse the arguments, type, required or not, help if something wrong, etc...
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id!")

    # We need to authenticate before we call the GET
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)  # Returns an object

        if item:
            return item.json()

        return {'message': "Item not found."}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        # if there is more arguments it doesn't matter
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        item.save_to_db()

        return item.json(), 201  # 201 status is for created! I also can say 202 the request had been accepted

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {'message': "Item deleted."}

    def put(self, name):  # PUT is idempotent operation

        # if there is more arguments it doesn't matter
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}  # Returns all the objects in the db
    # Or : return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
