from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure your SQLite database URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'

# Initialize SQLAlchemy
db = SQLAlchemy(app)