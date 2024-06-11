#code-1: 

# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # PostgreSQL configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:srushti@localhost:5432/tododb'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     completed = db.Column(db.Boolean, default=False)
#     subtasks = db.relationship('Subtask', backref='task', cascade='all, delete-orphan')

# class Subtask(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     completed = db.Column(db.Boolean, default=False)
#     task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

# @app.route('/')
# def index():
#     tasks = Task.query.all()
#     return render_template('index.html', tasks=tasks)

# @app.route('/add_task', methods=['POST'])
# def add_task():
#     content = request.form['content']
#     new_task = Task(content=content)
#     db.session.add(new_task)
#     db.session.commit()
#     return redirect(url_for('index'))

# @app.route('/delete_task/<int:id>', methods=['POST'])
# def delete_task(id):
#     task_to_delete = Task.query.get_or_404(id)
#     db.session.delete(task_to_delete)
#     db.session.commit()
#     return redirect(url_for('index'))

# @app.route('/complete_task/<int:id>', methods=['POST'])
# def complete_task(id):
#     task = Task.query.get_or_404(id)
#     task.completed = True
#     db.session.commit()
#     return redirect(url_for('index'))

# @app.route('/incomplete_task/<int:id>', methods=['POST'])
# def incomplete_task(id):
#     task = Task.query.get_or_404(id)
#     task.completed = False
#     db.session.commit()
#     return redirect(url_for('index'))

# @app.route('/add_subtask/<int:task_id>', methods=['POST'])
# def add_subtask(task_id):
#     task = Task.query.get_or_404(task_id)
#     content = request.form['content']
#     new_subtask = Subtask(content=content, task=task)
#     db.session.add(new_subtask)
#     db.session.commit()
#     return redirect(url_for('index'))

# @app.route('/delete_subtask/<int:subtask_id>', methods=['POST'])
# def delete_subtask(subtask_id):
#     subtask_to_delete = Subtask.query.get_or_404(subtask_id)
#     db.session.delete(subtask_to_delete)
#     db.session.commit()
#     return redirect(url_for('index'))

# @app.route('/complete_subtask/<int:subtask_id>', methods=['POST'])
# def complete_subtask(subtask_id):
#     subtask = Subtask.query.get_or_404(subtask_id)
#     subtask.completed = True
#     db.session.commit()
#     return redirect(url_for('index'))

# @app.route('/incomplete_subtask/<int:subtask_id>', methods=['POST'])
# def incomplete_subtask(subtask_id):
#     subtask = Subtask.query.get_or_404(subtask_id)
#     subtask.completed = False
#     db.session.commit()
#     return redirect(url_for('index'))

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)

#the above code is using SQLAlchemy






#code -2 :

#the code below is without using  SQLAlchemy

# from flask import Flask, render_template, request, redirect, url_for
# import psycopg2
# from psycopg2.extras import RealDictCursor

# app = Flask(__name__)

# # PostgreSQL configuration
# DB_HOST = "localhost"
# DB_NAME = "tododb"
# DB_USER = "postgres"
# DB_PASS = "srushti"

# def get_db_connection():
#     conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
#     return conn

# @app.route('/')
# def index():
#     conn = get_db_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)
    
#     # Fetch tasks
#     cur.execute("SELECT * FROM tasks")
#     tasks = cur.fetchall()
    
#     # Fetch subtasks and associate them with their tasks
#     for task in tasks:
#         cur.execute("SELECT * FROM subtasks WHERE task_id = %s", (task['id'],))
#         subtasks = cur.fetchall()
#         task['subtasks'] = subtasks
    
#     cur.close()
#     conn.close()
    
#     return render_template('index.html', tasks=tasks)

# @app.route('/add_task', methods=['POST'])
# def add_task():
#     content = request.form['content']
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("INSERT INTO tasks (content) VALUES (%s)", (content,))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return redirect(url_for('index'))

# @app.route('/delete_task/<int:id>', methods=['POST'])
# def delete_task(id):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
#     cur.execute("DELETE FROM subtasks WHERE task_id = %s", (id,))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return redirect(url_for('index'))

# @app.route('/complete_task/<int:id>', methods=['POST'])
# def complete_task(id):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("UPDATE tasks SET completed = TRUE WHERE id = %s", (id,))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return redirect(url_for('index'))

# @app.route('/incomplete_task/<int:id>', methods=['POST'])
# def incomplete_task(id):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("UPDATE tasks SET completed = FALSE WHERE id = %s", (id,))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return redirect(url_for('index'))

# @app.route('/add_subtask/<int:task_id>', methods=['POST'])
# def add_subtask(task_id):
#     content = request.form['content']
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("INSERT INTO subtasks (content, task_id) VALUES (%s, %s)", (content, task_id))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return redirect(url_for('index'))

# @app.route('/delete_subtask/<int:subtask_id>', methods=['POST'])
# def delete_subtask(subtask_id):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("DELETE FROM subtasks WHERE id = %s", (subtask_id,))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return redirect(url_for('index'))

# @app.route('/complete_subtask/<int:subtask_id>', methods=['POST'])
# def complete_subtask(subtask_id):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("UPDATE subtasks SET completed = TRUE WHERE id = %s", (subtask_id,))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return redirect(url_for('index'))

# @app.route('/incomplete_subtask/<int:subtask_id>', methods=['POST'])
# def incomplete_subtask(subtask_id):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("UPDATE subtasks SET completed = FALSE WHERE id = %s", (subtask_id,))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return redirect(url_for('index'))

# if __name__ == "__main__":
#     app.run(debug=True)


#table structures:

# CREATE TABLE tasks (
#     id SERIAL PRIMARY KEY,
#     content VARCHAR(200) NOT NULL,
#     completed BOOLEAN DEFAULT FALSE
# );

# CREATE TABLE subtasks (
#     id SERIAL PRIMARY KEY,
#     content VARCHAR(200) NOT NULL,
#     completed BOOLEAN DEFAULT FALSE,
#     task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE
# );


#code for different users login and adding tasks:

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# PostgreSQL configuration
DB_HOST = "localhost"
DB_NAME = "tododb"
DB_USER = "postgres"
DB_PASS = "srushti"

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return User(id=user['id'], username=user['username'])
    return None

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            flash('User registered successfully!', 'success')
        except Exception as e:
            flash('User registration failed!', 'danger')
            print(e)
        finally:
            cur.close()
            conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            login_user(User(id=user['id'], username=user['username']))
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Fetch tasks
    cur.execute("SELECT * FROM tasks WHERE user_id = %s", (current_user.id,))
    tasks = cur.fetchall()
    
    # Fetch subtasks and associate them with their tasks
    for task in tasks:
        cur.execute("SELECT * FROM subtasks WHERE task_id = %s", (task['id'],))
        subtasks = cur.fetchall()
        task['subtasks'] = subtasks
    
    cur.close()
    conn.close()
    
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    content = request.form['content']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (content, user_id) VALUES (%s, %s)", (content, current_user.id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete_task/<int:id>', methods=['POST'])
@login_required
def delete_task(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (id, current_user.id))
    cur.execute("DELETE FROM subtasks WHERE task_id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete_task/<int:id>', methods=['POST'])
@login_required
def complete_task(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed = TRUE WHERE id = %s AND user_id = %s", (id, current_user.id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/incomplete_task/<int:id>', methods=['POST'])
@login_required
def incomplete_task(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed = FALSE WHERE id = %s AND user_id = %s", (id, current_user.id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/add_subtask/<int:task_id>', methods=['POST'])
@login_required
def add_subtask(task_id):
    content = request.form['content']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO subtasks (content, task_id, user_id) VALUES (%s, %s, %s)", (content, task_id, current_user.id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete_subtask/<int:subtask_id>', methods=['POST'])
@login_required
def delete_subtask(subtask_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM subtasks WHERE id = %s AND user_id = %s", (subtask_id, current_user.id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete_subtask/<int:subtask_id>', methods=['POST'])
@login_required
def complete_subtask(subtask_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE subtasks SET completed = TRUE WHERE id = %s AND user_id = %s", (subtask_id, current_user.id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/incomplete_subtask/<int:subtask_id>', methods=['POST'])
@login_required
def incomplete_subtask(subtask_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE subtasks SET completed = FALSE WHERE id = %s AND user_id = %s", (subtask_id, current_user.id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
