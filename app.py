from flask import Flask, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Task(db.Model, JsonModel):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text())
    is_done = db.Column(db.Boolean(), default=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

@app.route('/add', methods=['POST'])
def submit():
    name = request.json.get('name')
    description = request.json.get('description')
    if name == '' or name.isspace():
        return jsonify(name ='Name cannot be empty'), 400
    if len(name)>100:
        return jsonify(name ='Name is too long'), 400
    if db.session.query(Task).filter(Task.name == name).count() == 0:
        data = Task(name, description)
        db.session.add(data)
        db.session.commit()
        return json.dumps([u.as_dict() for u in Task.query.all()]), 201
    return jsonify(name ='Task with the same name already exists'), 400

@app.route('/tasks', methods = ['GET'])
def index():
    return json.dumps([u.as_dict() for u in Task.query.all()])

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.filter_by(id=id).first()
    task.is_done = not task.is_done
    db.session.commit()
    return json.dumps([u.as_dict() for u in Task.query.all()])

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    Task.query.filter_by(id=id).delete()
    db.session.commit()
    return json.dumps([u.as_dict() for u in Task.query.all()])

if __name__ == '__main__':
    app.debug = True
    app.run()