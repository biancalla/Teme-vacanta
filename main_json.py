import json
import uuid
import re

# dupa ce am instalat libraria cu: pip install flask
from flask import Flask, request, Response

app = Flask(__name__)

def read_database(db_file="library_db.json"):
    with open(db_file, "r") as f:
        db_dict = json.load(f)
    return db_dict

def write_database(data_dict, db_file="library_db.json"):
    with open(db_file, "w") as f:
        json.dump(data_dict, f, indent=4)

def is_email_valid(email):
    email_regex = r'^[^@]+@[^@]+\.[^@]{2,}$'
    return re.match(email_regex, email) is not None

def is_user_data_valid(user_data):
    required_fields = {"name", "email", "password", "is_logged"}
    if not required_fields.issubset(user_data.keys()):
        return False

    if not is_email_valid(user_data["email"]):
        return False

    return True

# Users APIs
# read all users
@app.route("/users", methods=["GET"])
def read_all_users():
    db = read_database()
    list_of_users = db["users"]
    if list_of_users:
        return Response(status=200, response=json.dumps(list_of_users))
    else:
        return Response(status=404, response=json.dumps(f"No users has been found in DB!"))



# read user by email
@app.route("/users/<email>", methods=["GET"])
def get_user_by_email(email):
    db = read_database()
    for elem in db['users']:
        if elem['email'] == email:
            return Response(status=200, response=json.dumps(elem))
    return Response(status=404, response=json.dumps(f"No user with email {email} has been found in DB!"))


# add user
@app.route("/users/add", methods=["POST"])
def add_user():
    user_data = json.loads(request.data)

    if not is_user_data_valid(user_data):
        return Response(status=400, response=json.dumps({"reponse_message": "Invalid user data"}))

    user_id = str(uuid.uuid4()) # asignam un uuid random noului user
    user_data['id'] = user_id

    db = read_database()
    db["users"].append(user_data)
    write_database(db)
    return Response(status=201, response=json.dumps({"response_message": f"User with id {user_id} has been successfully created"}))

# Posibile imbunatatiri:
# 1. Verificam ca email-ul este valid 
# 2. Ne asiguram ca introducem doar field-urile potrivite in db
# de ex, userul urmator ar trebui sa dea eroare la add_user:
# {
#     "name": "abc",
#     "email": "abc.com",   # email invalid
#     "password": "1234",
#     "is_logged": false,
#     "age": 30,            # camp suplimentar
#     "id": "cba4ce26-c7e1-493c-b3d9-2eeb40d16b69"
# }
# 3. Adaugam o baza de date "adevarata", in speta un sqlite
# 4. Restructuram aplicatia in: app.py (contine API endpoint-urile), 
# database.py (contine functiile de creare si handling al db-ului), 
# crud.py (contine functiile query asupra db-ului)
# models.py (contine declararea claselor model care se ocupa cu obiectele)

if __name__ == '__main__':  # prima linie de cod care se citeste (dupa import-uri) in momentul in care rulam fisierul ca un script: python main.py
    app.run(debug=True, port=7000)