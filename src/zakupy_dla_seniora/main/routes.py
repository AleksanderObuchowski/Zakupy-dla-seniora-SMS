from flask import Blueprint, render_template, request
import json
main = Blueprint('main', __name__)
import requests
@main.route('/')
def home():
    return "<h1>Hello</h1>"
@main.route('/board_test')
def leaderboard():

    r = requests.get('http://127.0.0.1:5000/board')
    return render_template('board.html', data = r.json())
@main.route('/leaderboard')
def board():

    r = requests.get('http://127.0.0.1:5000/leaderboards')
    return render_template('leaderboard.html', data = r.json())
@main.route('/profile_view')
def profile():
    # to jest hardcodowane na 1 tak dla testów
    r = requests.get('http://127.0.0.1:5000/profile',params={"user_id":"6"})
    print(r.json())
    return render_template('profile.html', data = r.json())
@main.route('/take_order')
def take():

    # to jest hardcodowane na 1 tak dla testów
    print(request.args)
    r = requests.post('http://127.0.0.1:5000/placing',params=request.args)
    print(r.json())
    r = requests.get('http://127.0.0.1:5000/board')
    print(r.json())
    return render_template('board.html', data = r.json())
@main.route('/sent_end_placing')
def end():

    # to jest hardcodowane na 1 tak dla testów
    print(request.args)
    r = requests.post('http://127.0.0.1:5000/end_placing',params=request.args)
    print(r.json())
    r = requests.get('http://127.0.0.1:5000/profile',params={"user_id":"2"})
    return render_template('profile.html', data = r.json())