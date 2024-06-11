# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# db = SQLAlchemy(app)

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)

# @app.route('/')
# def index():
#     todos = Todo.query.all()
#     return render_template('index.html', todos=todos)

# @app.route('/add', methods=['POST'])
# def add_todo():
#     content = request.form['content']
#     new_todo = Todo(content=content)
#     db.session.add(new_todo)
#     db.session.commit()
#     return redirect(url_for('index'))

# @app.route('/delete/<int:id>')
# def delete_todo(id):
#     todo_to_delete = Todo.query.get_or_404(id)
#     db.session.delete(todo_to_delete)
#     db.session.commit()
#     return redirect(url_for('index'))

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db_file = os.path.join(os.path.dirname(__file__), 'todo.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    todos = Todo.query.all()
    print(f"Fetching todos: {todos}")  # Debug print
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    content = request.form['content']
    print(f"Adding todo: {content}")  # Debug print
    new_todo = Todo(content=content)
    db.session.add(new_todo)
    db.session.commit()
    print(f"Todo added: {new_todo}")  # Debug print
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_todo(id):
    todo_to_delete = Todo.query.get_or_404(id)
    print(f"Deleting todo: {todo_to_delete}")  # Debug print
    db.session.delete(todo_to_delete)
    db.session.commit()
    print(f"Todo deleted: {todo_to_delete}")  # Debug print
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created.")
    app.run(debug=True)
