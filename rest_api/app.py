from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store_data.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Creating book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False, unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

# Creating Book Schema
class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price')

# initializing schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)

# add a book into db
@app.route('/book', methods = ['POST'])
def add_book():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']

    new_book = Book(name, description, price)
    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book)

# get all books
@app.route('/get_all_books/', methods = ['GET'])
def get_all_books():
    book = Book.query.all()
    result = books_schema.dump(book)
    print (result, type(result), "hello")
    return jsonify(result)

# get a book
@app.route('/get_book/<id>', methods = ['GET'])
def get_book(id):
    book = Book.query.get(id)
    result = book_schema.dump(book)
    return jsonify(result)

# update a book into db
@app.route('/update_book/<id>', methods = ['PUT'])
def update_book(id):
    book = Book.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']

    book.name = name
    book.description = description
    book.price = price

    db.session.add(book)
    db.session.commit()

    return book_schema.jsonify(book)

# delete a book from db
@app.route('/delete_book/<id>', methods = ['DELETE'])
def delete_book(id):
    book = Book.query.get(id)

    db.session.delete(book)
    db.session.commit()

    return book_schema.jsonify(book)

if __name__ == '__main__':
    app.run(debug=True)