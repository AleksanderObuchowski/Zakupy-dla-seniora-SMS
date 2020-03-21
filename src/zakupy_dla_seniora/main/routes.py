from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, current_user, logout_user
from zakupy_dla_seniora import sql_db as db, bcrypt
from zakupy_dla_seniora.users.models import User
import requests

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/board_view')
def leaderboard():
    r = requests.get('http://127.0.0.1:5000/board')
    return render_template('board.html', data=r.json())


@main.route('/leaderboard')
def board():
    r = requests.get('http://127.0.0.1:5000/leaderboards')
    print(r.text)
    return render_template('leaderboard.html', data=r.json())


@main.route('/profile_view')
def profile():
    r = requests.get('http://127.0.0.1:5000/profile', params={"user_id": current_user.id})
    return render_template('profile.html', data=r.json())


@main.route('/take_order')
def take():
    r = requests.post('http://127.0.0.1:5000/placing', params=request.args)
    r = requests.get('http://127.0.0.1:5000/board')
    return render_template('board.html', data=r.json())


@main.route('/send_end_placing')
def end():
    r = requests.post('http://127.0.0.1:5000/end_placing', params=request.args)
    r = requests.get('http://127.0.0.1:5000/board')
    return render_template('board.html', data=r.json())


# LOGIN ROUTES

@main.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if current_user.is_authenticated:
        return redirect(url_for('main.board'))
    if request.method == 'POST':
        user = User.query.filter_by(display_name=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password_hash, request.form['password']):
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
        User(display_name=request.form['username'], email=request.form['email'], password=hashed_password).save()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', message=error_message)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.board'))