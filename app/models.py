from app import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


if __name__ == "__main__":
    db.metadata.clear()
# 下面几行取消注释后，可单独迁移数据库配置，但是无法去整个项目进行交互
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:guilin@localhost:3306/test?charset=utf8"
# app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)
# db.init_app(app)
manage = Manager(app)
migrate = Migrate(app, db)
manage.add_command('db', MigrateCommand)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % self.body


class SysUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=True, nullable=False)
    sysname = db.Column(db.String(200), index=True, unique=True, nullable=False)

    def __repr__(self):
        return '<SysUser %r>' % self.name


# models.py模块可以单独来执行，但是必须要有下面这段否则更新表结构后，无法建立迁移文件
if __name__ == "__main__":
    manage.run()
