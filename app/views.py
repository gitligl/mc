from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'ligl', 'email': 'ligl@123.com'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'A terrible day!'
        },
        {
            'author': {'username': 'Susan', 'email': 'susan@123.com'},
            'body': 'I am a beautiful girl...'
        }
    ]
    return render_template('index.html',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/home')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/home')
def home():
    return render_template('home.html')