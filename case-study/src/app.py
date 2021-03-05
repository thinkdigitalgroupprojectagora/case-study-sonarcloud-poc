from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time


# Wait until database is ready
print("Waiting for database to be ready...", flush= True)
time.sleep(3)

# Initiate flask
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dbMode=os.getenv("DB_MODE")
if dbMode == "postgresql":
    print("Using postgresql mode", flush=True)
    host=os.getenv("DB_HOST")
    port=os.getenv("DB_PORT")
    database=os.getenv("DB_NAME")
    username=os.getenv("DB_USER")
    password=os.getenv("DB_PASSWORD")
    DATABASE_URI = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
else:
    print("Using sqlite mode", flush=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"

# Initiate database
db = SQLAlchemy(app)

# Define data model
class User(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String())
    lastName = db.Column(db.String())

    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName

##Do the schema migrations
with app.app_context():
    db.create_all()

# Import some dummy data
firstUser = User('Foo', 'Bar')
db.session.add(firstUser)
db.session.commit()


# Define flask routes
@app.route('/')
def hello():
    return "Hello World! This version should be rollbacked, please roll me back, :)"

@app.route('/users/', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        # users = User.query.all()
        return jsonify(list(map(lambda user : {"id": user.__dict__["id"],"firstName":user.__dict__["firstName"], "lastName":user.__dict__["lastName"] }, User.query.all()))), 200
    else:
        payload = request.get_json(force=True)
        print(payload, flush=True)
        if "lastName" not in payload.keys() or "firstName" not in payload.keys():
            return "InvalidParameters", 400
        userToAdd = User(payload["firstName"], payload["lastName"])
        db.session.add(userToAdd)
        db.session.commit()

        return jsonify({"id": userToAdd.id,"firstName":userToAdd.firstName, "lastName":userToAdd.lastName }), 200


    users = User.query.all()
    return jsonify(list(map(lambda user : {"id": user.__dict__["id"],"firstName":user.__dict__["firstName"], "lastName":user.__dict__["lastName"] }, users))), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0")