from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_user, current_user, logout_user
from flaskblog import db, bcrypt
from zakupy_dla_seniora.users.models import User
main = Blueprint('main', __name__)
import requests

@main.route('/')
def home():
    return "<h1>Hello</h1>"
@main.route('/board_test')
def board():
    r = requests.get('http://127.0.0.1:5000/board')
    print(r)
    return render_template('board.html', data = r.json())
@main.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if current_user.is_authenticated:
        return redirect(url_for('main.board'))
    if request.method == 'POST':
        user = User.query.filter(User.display_name=request.form['username']).first()
        if user and bcrypt.check_password_hash(User.password, request.form['password']):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.board'))
        else:
            error_message = "Wrong username or password."
            return render_template('login.html', title='Login', message=error_message)
    return render_template('login.html', title='Login')
@main.route('/register-user', methods=['GET', 'POST'])
def register_user():
    error_message = None
    if current_user.is_authenticated:
        return redirect(url_for('main.board'))
    if request.method == 'POST':
        if request.form['password'] == request.form['password_again']:
            hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        else:
            error_message = 'Passwords not match'
            return render_template('register.html', title='Register', message=error_message)
        user = User(display_name=request.form['username'], email=request.form['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', message=error_message)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.board'))