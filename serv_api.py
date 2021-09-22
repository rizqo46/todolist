from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init First main
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
	date = db.Column(db.String(20))


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

# Create a 'To do'
@app.route('/todo', methods = ['POST'])
def add_todo():
	title = request.json['title']
	description = request.json['description']
	date = request.json['date']

	new_todo = todo(title, description, date)
	db.session.add(new_todo)
	db.session.commit()

	return todo_schema.jsonify(new_todo)

# Read To do list
@app.route('/todo', methods = ['GET'])
def get():
	todo_list = todo.query.all()
	results = todos_schema.dump(todo_list)
	return jsonify(results)

# Update to do list
@app.route('/todo/<id>', methods = ['PUT'])
def update(id):
	atodo = todo.query.get(id)

	title = request.json['title']
	description = request.json['description']
	date = request.json['date']

	atodo.title = title
	atodo.description = description
	atodo.date = date

	db.session.commit()

	return todo_schema.jsonify(atodo)

# Delete
@app.route('/todo', methods=['DELETE'])
def delete_todo():
	id_todo = int(request.args.get('id'))
	atodo = todo.query.get(id_todo)

	db.session.delete(atodo)
	db.session.commit()

	return todo_schema.jsonify(atodo)
# Run server
if __name__ == '__main__':
	app.run(debug = True)