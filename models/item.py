from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    # Use id because it is useful
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        # SQLAchemy will handle the connection, cursor and even queries
        # If it does not found any row, it will convert into an object
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1, 1º row only

    def save_to_db(self):
        db.session.add(self)  # We can add multiple items and commit after
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
