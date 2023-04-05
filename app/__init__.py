from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
db= SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

print("Hello")
print("zdivyn")


