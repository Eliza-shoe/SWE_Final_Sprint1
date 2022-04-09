<<<<<<< HEAD
from flask import Flask, session, request, jsonify
from dotenv import find_dotenv, load_dotenv
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__, static_folder='../build')
CORS(app)
@app.route('/api', methods=["GET"])
@cross_origin()
def index():
    return jsonify("FlaskTest")

CORS(app)
@app.route('/', methods=["GET"])
def serve():
    return send_from_directory(app.static_folder, 'index.html')


def main():
    app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)
if __name__ == '__main__':
    main()
=======
from flask import Flask as f, render_template
import os
import flask_sqlalchemy as f_sql
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = f(__name__)
app.secret_key = "I am a secret key for the Final"
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

db = f_sql.SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB")
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
        "SQLALCHEMY_DATABASE_URI"
    ].replace("postgres://", "postgresql://")

chat_table = db.Table(
    # Table combining many to many relationship with reviews table
    "chat_table",
    db.Column("ct_id", db.Integer, db.ForeignKey("ct.id"), primary_key=True),
    db.Column("user_id", db.String(30), db.ForeignKey("user.gsu_id"), primary_key=True),
    db.Column(
        "chatroom_id", db.Integer, db.ForeignKey("chatroom.id"), primary_key=True
    ),
)


class User(db.Model):
    """Defines each user of program, connects to Comments"""

    __tablename__ = "user"
    id = db.Column(db.Integer, unique=True)
    gsu_id = db.Column(db.String(30), unique=True, primary_key=True, nullable=False)
    f_name = db.Column(db.String(30), unique=False, nullable=False)
    l_name = db.Column(db.String(50), unique=False, nullable=False)
    level = db.Column(db.String(20), unique=False, nullable=False)
    primary_major = db.Column(
        db.String(30), unique=False, nullable=False, default="undecided"
    )
    chat_table = db.relationship(
        "Ct",
        secondary="chat_table",
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )

    def __repr__(self):
        return f"{self.gsu_id}"


class Restaurant(db.Model):
    __tablename__ = "restaurant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=False)
    rating = db.Column(db.Float, default=0)
    price = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.name}"


class Chatroom(db.Model):
    __tablename__ = "chatroom"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    chat_table = db.relationship(
        "Ct",
        secondary="chat_table",
        lazy="subquery",
        backref=db.backref("chatrooms", lazy=True),
    )

    def __repr__(self):
        return f"{self.name}"


class Ct(db.Model):
    id = db.Column(db.Integer, primary_key=True)


db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


# Test
app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
>>>>>>> main
