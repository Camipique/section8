from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    # Use id because it is useful
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # This is a list of ItemModels, lazy dynamic makes it like a query
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

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
