from flask import Flask, render_template, g
from flask import request, url_for, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import hashlib
import functools

app = Flask(__name__)

app.secret_key = '840yOH3GHO9q'

@app.before_request
def load_logged_in_user():
    if 'uid' in session:
        g.user = session['uid']
    else:
        g.user = None
        return

#-----#
#IMPORTANT FUNCTIONS
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)
    return wrapped_view

def generate_session_id(uname):
    secure_id = hashlib.sha256(str(uname).encode()).hexdigest()
    return secure_id
#IMPORTANT FUNCTIONS
#-----#

#DEFAULT PAGE
@app.route("/")
def index():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    posts = cursor.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN users u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

#REGISTER
@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        error = None

        username = request.form['username']
        password = request.form['password']
        if not username:
            error='need username'
        if not password:
            error='need pwd'
        
        existing_user = cursor.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if existing_user:
            error = 'duplicate'
            return render_template('register.html')


        if error is None:
            try:
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                connection.commit()
            except connection.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('register.html')

#LOGIN
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        error = None
        username = request.form['username']
        password = request.form['password']
        user = cursor.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username or password.'
            return redirect(url_for('login'))
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'
            return redirect(url_for('login'))
            
        if error is None:
            session.clear()
            session['uid'] = generate_session_id(user)
            print(session['uid'])
            return redirect(url_for('home'))
        
    elif request.method == 'GET':
        return render_template('login.html')


#LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#HOME PAGE
@app.route('/home')
def home():
    if 'uid' in session:
        print(session['uid'])
        return "<p>home page</p>" 
    else:
        print('not logged in!')
        return redirect(url_for('index'))

#import blog
#app.register_blueprint(blog.bp)
#app.add_url_rule('/', endpoint='index')

#cd .\Documents\coding\flask_app01\
#flask --app app run
if __name__ == "__main__":
    app.run()