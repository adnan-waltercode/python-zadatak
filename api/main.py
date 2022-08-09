import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from routes import api
from config import SQLALCHEMY_URI, JWT_KEY
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_URI
app.config['JWT_KEY'] = JWT_KEY
db.init_app(app)
api.init_app(app)
CORS(app)

@app.before_first_request
def init_database():
    db.create_all()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)