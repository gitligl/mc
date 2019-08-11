from app import app, db
from flask import render_template, request
from app.models import User
import hashlib
from minio import Minio


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET'])
def login_form():
    return render_template('form.html')


@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    md5_password = hashlib.md5()
    md5_password.update(password.encode('utf-8'))
    if db.session.query(User).filter_by(username=username).all():
        if md5_password.hexdigest() == db.session.query(User).filter_by(username=username).all()[0].password:
            return render_template('login_ok.html', username=username)
    return render_template('form.html', message='Bad username or password', username=username)


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm']
    email = request.form['email']
    if password != confirm:
        return render_template('register.html', message='两次输入的密码不一致，请重新输入', username=username)
    md5_password = hashlib.md5()
    md5_password.update(password.encode('utf-8'))
    user = User(username=username, email=email, password=md5_password.hexdigest())
    db.session.add(user)
    db.session.commit()
    return render_template('form.html')


mc = Minio('106.15.236.58:19000',
           access_key='0BJ9Q4VGACHQCNSBP22O',
           secret_key='QabWEMjtkWHNanxsp5ZsF0vaumOU6wXNNgtPFMiJ',
           secure=False)


@app.route('/mc/api/v1/buckets', methods=['GET'])
def list_buckets():
    buckets = mc.list_buckets()
    count = len(buckets)
    buckets_dic = {}
    buckets_list = []
    buckets_dic['bucket_counts'] = count
    for bucket in buckets:
        buckets_list.append(bucket.name)
    buckets_dic['bucket_names'] = buckets_list
    return buckets_dic


@app.route('/mc/api/v1/buckets/<string:bucket_name>/', methods=['GET'])
def bucket_object(bucket_name):
    objects = mc.list_objects(bucket_name)
    objects_dic = {}
    objects_list = []
    objects_dic['bucket_name'] = bucket_name
    for obj in objects:
        objects_list.append(obj.object_name)
    objects_dic['objects_names'] = objects_list
    return objects_dic
