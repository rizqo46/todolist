from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init
app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))

# Data
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # Init DB
ma = Marshmallow(app)# Init Marshmallow

class todo(db.Model):
	"""docstring for todo"""
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	description = db.Column(db.String(200))
	date = db.Column(db.DateTime)


	def __init__(self, title, description, date):
		self.title = title
		self.description = description
		self.date = date

# 'To Do' Schema
class todoSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'description', 'date')

# Init schema
todo_schema = todoSchema()
todos_schema = todoSchema(many=True)
		


# Run server
if __name__ == '__main__':
	app.run(debug = True)