"""Scriptul de creare a bazei de date"""

import sqlite3

DB_FILE_PATH = "library_sqlite.db"  # constanta catre fisierul db-ului sqlite


def open_db(db_file_path=DB_FILE_PATH):
    try:
        connection = sqlite3.connect(db_file_path, check_same_thread=False)
    except Exception as e:
        raise e
    else:
        return connection  # returnam obiectul conexiune la DB


def create_db(db_file_path=DB_FILE_PATH):
    db_creation_sql = """
    CREATE TABLE IF NOT EXISTS Users (
    id TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    is_logged INTEGER NOT NULL DEFAULT 0 CHECK(is_logged IN (0,1))
    );

    CREATE TABLE IF NOT EXISTS Books (
    id TEXT NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    pages INTEGER NOT NULL,
    category TEXT NOT NULL
    );
    """ 

    # tabela Users
    #  id   |  name  |      email       | password  | is_logged 
    # uuid1 | primul | primul@mylib.com |    1111   |    0  (False) 
    # ...


    # tabela Books
    #  id   |     title     |   author   | pages |  category
    # ...

    with sqlite3.connect(db_file_path) as connection:   # deschidem conexiunea la db

        cursor = connection.cursor()   # cream ob cursor cu care rulam query
        cursor.executescript(db_creation_sql)         # executam query-ul SQL de creare a structurii DB-ului

        connection.commit()            #  commit-uim (salvam) fisierul db-ului

    # connection.close()  # nu mai e nevoie fiindca am folosit context manager-ul with

if __name__ == '__main__':
    create_db()