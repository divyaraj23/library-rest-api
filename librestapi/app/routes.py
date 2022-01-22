from flask import request, jsonify
from app import app,dbsetup



#API descriptions in readme.md
@app.route('/libapi/books/search_book/<book_name>', methods=['GET'])
def api_get_bookbyname(book_name):
    return jsonify(dbsetup.get_book_by_name(book_name))


@app.route('/libapi/books/add_book', methods=['POST'])
def api_add_book():
    book = request.get_json(force=True)
    return jsonify(dbsetup.add_book(book))

@app.route('/libapi/library/add_library', methods=['POST'])
def api_add_library():
    library = request.get_json(force=True)
    return jsonify(dbsetup.add_library(library))

@app.route('/libapi/users/add_user', methods=['POST'])
def api_add_user():
    user = request.get_json(force=True)
    return jsonify(dbsetup.add_user(user))

@app.route('/libapi/library/add_book', methods=['POST'])
def api_add_book_to_lib():
    book = request.get_json(force=True)
    return jsonify(dbsetup.add_book_to_library(book))

@app.route('/libapi/book/checkout_book', methods=['POST'])
def api_checkout_book():
    book = request.get_json(force=True)
    return jsonify(dbsetup.checkout_book(book))

@app.route('/libapi/book/checkin_book', methods=['POST'])
def api_checkin_book():
    book = request.get_json(force=True)
    return jsonify(dbsetup.checkin_book(book))