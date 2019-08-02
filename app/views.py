from app import app
from flask import render_template, request
from app.models import db, User


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET'])
def login_form():
    return render_template('form.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if db.session.query(User).filter_by(username=username).all():
        if password == db.session.query(User).filter_by(username=username).all()[0].password:
            return render_template('login_ok.html', username=username)
    return render_template('form.html', message='Bad username or password', username=username)
