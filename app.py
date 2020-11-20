from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
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
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        if name == '':
            return 'Name cannot be empty'
        if db.session.query(Task).filter(Task.name == name).count() == 0:
            data = Task(name, description)
            db.session.add(data)
            db.session.commit()
            return 'Success'
        return 'Task with the same name already exists'

if __name__ == '__main__':
    app.debug = True
    app.run()