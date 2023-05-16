"""Scriptul main unde avem API endpoint-urile"""
import json

# dupa ce am instalat libraria cu: pip install flask
from flask import Flask, request, Response

import crud_sqlite as crud


from database_sqlite import open_db

app = Flask(__name__)
db_connection = open_db()  # ne cream o conexiune globala la DB pe care sa o refolosim in toate API-urile 


# API endpoints

# get all users
@app.route("/users", methods=["GET"])
def read_all_users():
    def format_user(user):
        return {
            "name": user.name,
            "email": user.email,
            "is_logged": user.is_logged
        }
    # TODO: trebuie afisat user-ul mai citet, cu parola ascunsa si id scos din raspuns!!
    status_code, response_body = crud.get_users(db_connection)  # apelam functia crud care se ocupa de extragerea datelor necesare din db
    formatted_users = [format_user(user) for user in users]
    return Response(status=status_code, response=json.dumps(formatted_users))  # returnam response-ul catre client


# add user
@app.route("/users/add_user", methods=["POST"])
def create_user():
    user_data = json.loads(request.data)  # luam datele de adaugam de pe body-ul requestului
    status_code, response_body = crud.add_user(db_connection, user_data)
    return Response(status=status_code, response=json.dumps(response_body))


# update user
@app.route("/users/update_user/<user_id>", methods=["PATCH", "PUT"])
def update_user(user_id):
    user_data = json.loads(request.data)    

    if request.method == "PATCH":  # update partial (doar la campurile trimise de client)
        status_code, response_body = crud.update_user(db_connection, user_id, user_data)

    elif request.method == "PUT":  # update integral (client trimite toate campurile User)
        status_code, response_body = crud.update_user_put(db_connection, user_id, user_data)

    # else:   # nu e nevoie sa handle-uim methodele care nu sunt trecute in methods
    #     status_code, response_body = 400, f"Request method invalid.."

    return Response(status=status_code, response=json.dumps(response_body))


# delete user
@app.route("/users/delete_user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    status_code, response_body = crud.delete_user(db_connection, user_id)    
    return Response(status=status_code, response=json.dumps(response_body))

# get user by id
@app.route("/users/get_user/<user_id>", methods=["GET"])
def get_user():
    db = read_database()
    for user in db["users"]:
        if user["id"] == user_id:
            return Response(status=200, response=json.dumps(user))
    return Response(status=404, response=json.dumps({"response_message": f"No user with id {user_id} has been found in the DB."}))


# TODO: addaugati API-urile similare pentru Books (pana marti!!!) + get_book_by_id si get_user_by_id
# API endpoints

# get all books
@app.route("/books", methods=["GET"])
def read_all_books():
    def format_book(book):
        return {
            "title": book.title,
            "author": book.author,
            "pages": book.pages,
            "category": book.category
        }

    status_code, response_body = crud.get_books(db_connection)  # apelam functia crud care se ocupa de extragerea datelor necesare din db
    formatted_books = [format_book(book) for book in books]
    return Response(status=status_code, response=json.dumps(formatted_books))  # returnam response-ul catre client


# add book
@app.route("/books/add_book", methods=["POST"])
def create_book():
    book_data = json.loads(request.data)  # luam datele de adaugam de pe body-ul requestului
    status_code, response_body = crud.add_book(db_connection, book_data)
    return Response(status=status_code, response=json.dumps(response_body))


# update book
@app.route("/books/update_book/<book_id>", methods=["PATCH", "PUT"])
def update_book(book_id):
    book_data = json.loads(request.data)

    if request.method == "PATCH":  # update partial (doar la campurile trimise de client)
        status_code, response_body = crud.update_book(db_connection, book_id, book_data)

    elif request.method == "PUT":  # update integral (client trimite toate campurile User)
        status_code, response_body = crud.update_book_put(db_connection, book_id, book_data)

    # else:   # nu e nevoie sa handle-uim methodele care nu sunt trecute in methods
    #     status_code, response_body = 400, f"Request method invalid.."

    return Response(status=status_code, response=json.dumps(response_body))


# delete book
@app.route("/books/delete_book/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    status_code, response_body = crud.delete_book(db_connection, user_id)
    return Response(status=status_code, response=json.dumps(response_body))

# get book by id
@app.route("/books/get_book/<book_id>", methods=["GET"])
def get_book():
    db = read_database()
    for book in db["books"]:
        if book["id"] == book_id:
            return Response(status=200, response=json.dumps(book))
    return Response(status=404, response=json.dumps({"response_message": f"No book with id {book_id} has been found in the DB."}))

if __name__ == '__main__':  # prima linie de cod care se citeste (dupa import-uri) in momentul in care rulam fisierul ca un script: python main.py
    app.run(debug=True, port=7000)