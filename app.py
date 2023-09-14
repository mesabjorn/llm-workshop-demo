from flask import Flask, render_template, request, redirect, url_for, flash,session
from werkzeug.security import generate_password_hash,check_password_hash

from models.User import db, User

app = Flask(__name__)

# Configure your SQLite database URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'


from db import init_db,register_init_db_command

register_init_db_command(app) # let user init database with cli
init_db(app)

app.secret_key = 'your_secret_key'  # Set a secret key for session management

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user input from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username or email is already in use
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email address already registered. Please use a different one.', 'danger')
            return redirect(url_for('register'))

        # Hash the password for security
        hashed_password = generate_password_hash(password, method='sha256')

        # Create a new user and add it to the database
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the user by username
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # If the user exists and the password is correct, log them in
            session['user_id'] = user.id  # Store the user's ID in the session
            session['username'] = user.username  # Store the user's ID in the session
            flash('Login successful!', 'success')
            return redirect('/')  # Redirect to the homepage
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():    
    session.clear()

    return redirect('/')  # Redirect to the homepage
        

@app.route('/', methods=['GET'])
def index():
    if 'username' in session:
        return render_template('index.html',user=session['username'])
    return render_template('index.html',user="")