from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Author(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     first_name = db.Column(db.String(80), nullable=False)
     last_name = db.Column(db.String(80), nullable=False)
     books = db.relationship('Books', backref='author', lazy=True)

class Books(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title_books = db.Column(db.String(80), nullable=False)
     number_of_instances = db.Column(db.Integer, nullable=False)
     year_of_publication = db.Column(db.DateTime, default=datetime.utcnow)
     author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(80), unique=True, nullable=False)
     email = db.Column(db.String(120), unique=True, nullable=False)
     password = db.Column(db.String(128), nullable=False)
     created_at = db.Column(db.DateTime, default=datetime.utcnow)

     def set_password(self, password):
          self.password_hash = generate_password_hash(password)


     def check_password(self, password):
          return check_password_hash(self.password_hash, password)

