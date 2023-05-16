"""Functiile CRUD asupra DB-ului"""
import uuid
from sqlite3 import Row

# APP de imports: python are probleme cu importurile circulare!! solutii: 1. restructurarea modulelor, 2. importarea intregului modul nu doar a unor functii/clase anume, 3...

from models_sqlite import User, Book

def get_users(db_connection):
    # functia CRUD de returnare a tuturor userilor din DB.
    # rulam un sql query si returnam un status_code si un mesaj/date
    # daca avem exceptie pe DB, returnam 500 si mesajul exceptiei, 
    # daca nu avem useri in db returnam 404 si mesajul "No users...",
    # iar daca totul functioneaza corect, returnam 200 si lista de useri
    SQL_QUERY = "SELECT * FROM Users;"
    try:
        cursor = db_connection.cursor()
        cursor.execute(SQL_QUERY)  # executam sql query-ul
    except Exception as e:
        return 500, f"Server error: {e}"
    else:
        users = cursor.fetchall()
        if users:
            return 200, users
        else:
            return 404, f"No users in DB!"


def add_user(db_connection, user_data):
    user_data['id'] = str(uuid.uuid4())   # datele introduse de client
    user_obj = User(**user_data)          # cream obiectul User (care seteaza si is_logged)
    if not user_obj.validate():
        return 400, f"User validation error!"

    SQL_QUERY = "INSERT INTO Users(id, name, password, email, is_logged) VALUES (:id, :name, :password, :email, :is_logged);"
    try:
        cursor = db_connection.cursor()
        cursor.execute(SQL_QUERY, user_obj.__dict__)  # inlocuim VALUES din SQL_QUERY cu valorile adevarate din dict-ul aferent obiectului user_obj 
        db_connection.commit()
    except Exception as e:
        return 500, f"Server error: {e}"
    else:
        return 201, f"User with id={user_data['id']} has been successfully created!"


def update_user(db_connection, user_id, user_data):
    # 1. identificam userul in db pe baza user_id
    # 2. ne asiguram ca exista, in caz contrar returnam 404
    # 3. instantiem un obiect User si validam datele
    # 4. updatam userul in baza de date
    # user_data = {"name": "John Doe"}
    try:
        del user_data['id']   # ne asiguram ca pe request nu se trimite in dict si cheia 'id', fiindca in general id-ul nu poate fi modificat
    except:
        pass
    SQL_QUERY = "SELECT * FROM Users WHERE id=?;"
    try:
        cursor = db_connection.cursor()
        cursor.row_factory = Row   # modificam tipul de date returnat de cursor pt a inlocui tupla default cu un dict
        cursor.execute(SQL_QUERY, (user_id,))  # atentie, functia cursor.execute asteapta ca valori de inlocuit in query o tupla!!! 
    except Exception as e:
        return 500, f"Server error: {e}"
    else:
        user_from_db = cursor.fetchone()       # returnam user-ul din db
        if user_from_db:                       # verificam ca nu e None 
            user_from_db = dict(user_from_db)  # daca nu e None, putem apela dict() datorita faptului ca avem row_factory setat ca Row
            user_from_db.update(user_data)     # actualizam userul din db cu dictionarul user_data
            user_obj = User(**user_from_db)    # cream obiectul User pentru a valida datele
            if not user_obj.validate():        # validam datele
                return 400, f"User validation error!"
            # SQL_QUERY = "UPDATE User (id, name, password, email, is_logged) SET VALUES (:id, :name, :password, :email, :is_logged) WHERE id=:id;"
            SQL_QUERY = "UPDATE Users SET id=:id, name=:name, password=:password, email=:email, is_logged=:is_logged WHERE id=:id;"

            try: 
                cursor.execute(SQL_QUERY, user_obj.__dict__)
                db_connection.commit()         # cand adaugam/updatam/stergem randuri din DB trebuie sa dam commit
            except Exception as e:
                return 500, f"Server error: {e}"
            else:
                return 200, f"User with id={user_id} has been successfully updated: {user_obj.__dict__}"
        else:
            return 404, f"User with id={user_id} has not been found in DB!"


def update_user_put(db_connection, user_id, user_data):
    # in cazul requestului de tip PUT, actualizarea se face integral (la toate campurile)
    # asa ca trebuie verificat ca user_data sa contina toate campurile
    SQL_QUERY = "UPDATE Users SET id=:id, name=:name, password=:password, email=:email, is_logged=:is_logged WHERE id=:id;" 
    try:
        user_obj = User(**user_data)
    except TypeError:
        return 400, f"User fields missing..."
    else:
        if not user_obj.validate():        # validam datele
            return 400, f"User validation error!"
        try:
            cursor = db_connection.cursor()
            cursor.execute(SQL_QUERY, user_obj.__dict__)
            db_connection.commit()
        except Exception as e:
            return 500, f"Server error: {e}"
        else:
            return 200, f"User with id={user_id} has been successfully updated with PUT: {user_obj.__dict__}"


def delete_user(db_connection, user_id):
    SQL_QUERY = "DELETE FROM Users WHERE id=?;"
    try:
        cursor = db_connection.cursor()
        cursor.execute(SQL_QUERY, (user_id,))
        db_connection.commit()
    except Exception as e:
        return 500, f"Server error: {e}"
    else:
        if cursor.rowcount:  # cursor.rowcount e un int, if e adevarat daca nu e 0
            return 200, f"User with id={user_id} has been successfully removed from DB!" 
        else:                # cursor.rowcount == 0 => niciun rand afectat 
            return 404, f"User with id={user_id} has not been found in DB!"


def get_books(db_connection):
    # functia CRUD de returnare a tuturor books din DB.
    # rulam un sql query si returnam un status_code si un mesaj/date
    # daca avem exceptie pe DB, returnam 500 si mesajul exceptiei,
    # daca nu avem books in db returnam 404 si mesajul "No books...",
    # iar daca totul functioneaza corect, returnam 200 si lista de books
    SQL_QUERY = "SELECT * FROM Books;"
    try:
        cursor = db_connection.cursor()
        cursor.execute(SQL_QUERY)  # executam sql query-ul
    except Exception as e:
        return 500, f"Server error: {e}"
    else:
        books = cursor.fetchall()
        if books:
            return 200, books
        else:
            return 404, f"No books in DB!"


def add_book(db_connection, book_data):
    book_data['id'] = str(uuid.uuid4())   # datele introduse de client
    book_obj = Book(**book_data)          # cream obiectul Book
    if not book_obj.validate():
        return 400, f"Book validation error!"

    SQL_QUERY = "INSERT INTO Books(id, title, author, pages, category) VALUES (:id, :title, :author, :pages, :category);"
    try:
        cursor = db_connection.cursor()
        cursor.execute(SQL_QUERY, book_obj.__dict__)  # inlocuim VALUES din SQL_QUERY cu valorile adevarate din dict-ul aferent obiectului book_obj
        db_connection.commit()
    except Exception as e:
        return 500, f"Server error: {e}"
    else:
        return 201, f"Book with id={book_data['id']} has been successfully created!"


def update_book(db_connection, book_id, book_data):
    # 1. identificam bookul in db pe baza book_id
    # 2. ne asiguram ca exista, in caz contrar returnam 404
    # 3. instantiem un obiect Book si validam datele
    # 4. updatam bookul in baza de date
    # book_data = {"title": "Amintiri din copilarie"}
    try:
        del book_data['id']   # ne asiguram ca pe request nu se trimite in dict si cheia 'id', fiindca in general id-ul nu poate fi modificat
    except:
        pass
    SQL_QUERY = "SELECT * FROM Books WHERE id=?;"
    try:
        cursor = db_connection.cursor()
        cursor.row_factory = Row   # modificam tipul de date returnat de cursor pt a inlocui tupla default cu un dict
        cursor.execute(SQL_QUERY, (book_id,))  # atentie, functia cursor.execute asteapta ca valori de inlocuit in query o tupla!!!
    except Exception as e:
        return 500, f"Server error: {e}"
    else:
        book_from_db = cursor.fetchone()       # returnam book-ul din db
        if book_from_db:                       # verificam ca nu e None
            book_from_db = dict(book_from_db)  # daca nu e None, putem apela dict() datorita faptului ca avem row_factory setat ca Row
            book_from_db.update(book_data)     # actualizam bookul din db cu dictionarul book_data
            book_obj = User(**book_from_db)    # cream obiectul Book pentru a valida datele
            if not book_obj.validate():        # validam datele
                return 400, f"Book validation error!"
            # SQL_QUERY = "UPDATE Book (id, title, author, pages, category) SET VALUES (:id, :title, :author, :pages, :category) WHERE id=:id;"
            SQL_QUERY = "UPDATE Books SET id=:id, title=:title, author=:author, pages=:pages, category=:category WHERE id=:id;"

            try:
                cursor.execute(SQL_QUERY, book_obj.__dict__)
                db_connection.commit()         # cand adaugam/updatam/stergem randuri din DB trebuie sa dam commit
            except Exception as e:
                return 500, f"Server error: {e}"
            else:
                return 200, f"Book with id={book_id} has been successfully updated: {book_obj.__dict__}"
        else:
            return 404, f"Book with id={book_id} has not been found in DB!"


def update_book_put(db_connection, book_id, book_data):
    # in cazul requestului de tip PUT, actualizarea se face integral (la toate campurile)
    # asa ca trebuie verificat ca book_data sa contina toate campurile
    SQL_QUERY = "UPDATE Books SET id=:id, title=:title, author=:author, pages=:pages, category=:category WHERE id=:id;"
    try:
        book_obj = Book(**book_data)
    except TypeError:
        return 400, f"Book fields missing..."
    else:
        if not book_obj.validate():        # validam datele
            return 400, f"Book validation error!"
        try:
            cursor = db_connection.cursor()
            cursor.execute(SQL_QUERY, book_obj.__dict__)
            db_connection.commit()
        except Exception as e:
            return 500, f"Server error: {e}"
        else:
            return 200, f"Book with id={book_id} has been successfully updated with PUT: {book_obj.__dict__}"


def delete_book(db_connection, user_id):
    SQL_QUERY = "DELETE FROM Books WHERE id=?;"
    try:
        cursor = db_connection.cursor()
        cursor.execute(SQL_QUERY, (book_id,))
        db_connection.commit()
    except Exception as e:
        return 500, f"Server error: {e}"
    else:
        if cursor.rowcount:  # cursor.rowcount e un int, if e adevarat daca nu e 0
            return 200, f"Book with id={book_id} has been successfully removed from DB!"
        else:                # cursor.rowcount == 0 => niciun rand afectat
            return 404, f"Book with id={book_id} has not been found in DB!"