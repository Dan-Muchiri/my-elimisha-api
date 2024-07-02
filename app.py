from flask import Flask, jsonify, request, make_response, session
from flask_restful import Resource,Api
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
from model import db
from flask_mail import Mail
from flask_mail import Message


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my-elimisha.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
mail = Mail(app)


api = Api(app)

CORS(app)
    

# Load environment variables from .env file
load_dotenv()

from model import db, User


@app.route('/')
def home():
    return 'Home!'



if __name__ == '__main__':
    with app.app_context():
        app.run(port=5050, debug=True)