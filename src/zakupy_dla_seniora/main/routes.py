from flask import Blueprint, render_template
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
