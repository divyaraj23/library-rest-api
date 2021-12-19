from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_book_by_name
from db import add_book
from db import initialize_db_tables
from db import add_library
from db import add_user
from db import add_book_to_library
from db import checkout_book
from db import checkin_book


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/libapi/books/search_book/<book_name>', methods=['GET'])
def api_get_bookbyname(book_name):
    return jsonify(get_book_by_name(book_name))

@app.route('/libapi/books/add_book', methods=['POST'])
def api_add_book():
    book = request.get_json(force=True)
    return jsonify(add_book(book))

@app.route('/libapi/library/add_library', methods=['POST'])
def api_add_library():
    library = request.get_json(force=True)
    return jsonify(add_library(library))

@app.route('/libapi/users/add_user', methods=['POST'])
def api_add_user():
    user = request.get_json(force=True)
    return jsonify(add_user(user))

@app.route('/libapi/library/add_book', methods=['POST'])
def api_add_book_to_lib():
    book = request.get_json(force=True)
    return jsonify(add_book_to_library(book))

@app.route('/libapi/book/checkout_book', methods=['POST'])
def api_checkout_book():
    book = request.get_json(force=True)
    return jsonify(checkout_book(book))

@app.route('/libapi/book/checkin_book', methods=['POST'])
def api_checkin_book():
    book = request.get_json(force=True)
    return jsonify(checkin_book(book))



if __name__ == "__main__":
    initialize_db_tables()
    app.run()
